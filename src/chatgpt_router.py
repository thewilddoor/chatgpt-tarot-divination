import json
import time
from typing import Optional
from fastapi.responses import StreamingResponse
from openai import OpenAI

import logging

from fastapi import Depends, HTTPException, Request, status


from src.config import settings
from fastapi import APIRouter

from src.models import DivinationBody, User
from src.user import get_user
from src.limiter import get_real_ipaddr, check_rate_limit
from src.divination import DivinationFactory
from src.session_manager import session_manager

client = OpenAI(api_key=settings.api_key, base_url=settings.api_base)
router = APIRouter()
_logger = logging.getLogger(__name__)
STOP_WORDS = [
    "忽略", "ignore", "指令", "命令", "command", "help", "帮助", "之前",
    "幫助", "現在", "開始", "开始", "start", "restart", "重新开始", "重新開始",
    "遵守", "遵循", "遵从", "遵從"
]


@router.post("/api/divination")
async def divination(
        request: Request,
        divination_body: DivinationBody,
        user: Optional[User] = Depends(get_user)
):

    real_ip = get_real_ipaddr(request)
    # rate limit when not login
    if settings.enable_rate_limit:
        if not user:
            max_reqs, time_window_seconds = settings.rate_limit
            check_rate_limit(f"{settings.project_name}:{real_ip}", time_window_seconds, max_reqs)
        else:
            max_reqs, time_window_seconds = settings.user_rate_limit
            check_rate_limit(
                f"{settings.project_name}:{user.login_type}:{user.user_name}", time_window_seconds, max_reqs
            )

    _logger.info(
        f"Request from {real_ip}, "
        f"user={user.model_dump_json(context=dict(ensure_ascii=False)) if user else None}, "
        f"body={divination_body.model_dump_json(context=dict(ensure_ascii=False))}"
    )
    
    # 检查是否为追问请求
    is_follow_up = divination_body.is_follow_up and divination_body.session_id
    session_id = None
    
    if is_follow_up:
        # 处理追问逻辑
        if not divination_body.follow_up_question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="追问内容不能为空"
            )
        
        session = session_manager.get_session(divination_body.session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="会话不存在或已过期"
            )
        
        if not session_manager.can_follow_up(divination_body.session_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"追问次数已达上限({session.max_follow_ups}次)"
            )
        
        # 增加追问次数
        session_manager.increment_follow_up(divination_body.session_id)
        
        # 处理追问逻辑 - 使用原始占卜类型的系统提示词
        session = session_manager.get_session(divination_body.session_id)
        original_divination = session.original_divination
        
        # 重建原始占卜请求，获取原始系统提示词
        original_prompt_type = original_divination.get("prompt_type")
        divination_obj = DivinationFactory.get(original_prompt_type)
        
        if not divination_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"原始占卜类型 {original_prompt_type} 不支持"
            )
        
        # 重建原始DivinationBody对象
        temp_body = type('TempDivinationBody', (), {
            'prompt': original_divination.get("prompt", ""),
            'prompt_type': original_prompt_type,
            'birthday': original_divination.get("birthday", ""),
            'plum_flower': None
        })()
        
        # 如果是梅花易数，重建plum_flower对象
        if original_prompt_type == "plum_flower" and original_divination.get("plum_flower"):
            plum_data = original_divination["plum_flower"]
            temp_body.plum_flower = type('PlumFlower', (), {
                'num1': plum_data.get("num1", 0),
                'num2': plum_data.get("num2", 0),
                'model_dump': lambda: plum_data
            })()
        
        # 获取原始的完整prompt和system_prompt
        original_full_prompt, system_prompt = divination_obj.build_prompt(temp_body)
        
        # 构建追问的用户输入（包含原始完整信息+追问）
        prompt = f"{original_full_prompt}\n\n【用户追问】\n{divination_body.follow_up_question}"
        
        session_id = divination_body.session_id
    else:
        # 处理首次占卜逻辑
        if any(w in divination_body.prompt.lower() for w in STOP_WORDS):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Prompt contains stop words"
            )
        
        divination_obj = DivinationFactory.get(divination_body.prompt_type)
        if not divination_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No prompt type {divination_body.prompt_type} not supported"
            )
        
        prompt, system_prompt = divination_obj.build_prompt(divination_body)
        
        # 创建新会话
        original_divination = {
            "prompt": divination_body.prompt,
            "prompt_type": divination_body.prompt_type,
            "birthday": divination_body.birthday,
            "plum_flower": divination_body.plum_flower.model_dump() if divination_body.plum_flower else None
        }
        session_id = session_manager.create_session(original_divination)

    # custom api key, model and base url support
    custom_base_url = request.headers.get("x-api-url")
    custom_api_key = request.headers.get("x-api-key")
    custom_api_model = request.headers.get("x-api-model")
    api_client = client
    api_model = custom_api_model if custom_api_model else settings.model
    if custom_base_url and custom_api_key:
        api_client = OpenAI(api_key=custom_api_key, base_url=custom_base_url)
    elif custom_api_key:
        api_client = OpenAI(api_key=custom_api_key, base_url=settings.api_base)

    if not (settings.api_base or custom_base_url) or not (settings.api_key or custom_api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请设置 API KEY 和 API BASE URL"
        )

    def get_ai_generator():
        # 构建消息列表
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        
        # 如果是追问，添加上下文消息并直接添加用户追问
        if is_follow_up:
            context_messages = session_manager.get_context_messages(session_id)
            messages.extend(context_messages)
            # 添加当前追问消息到会话历史
            session_manager.add_message(session_id, "user", divination_body.follow_up_question)
            messages.append({"role": "user", "content": prompt})
        else:
            # 首次占卜，直接添加用户消息
            messages.append({"role": "user", "content": prompt})
        
        ai_stream = api_client.chat.completions.create(
            model=api_model,
            max_tokens=8192,
            temperature=0.6,
            stream=True,
            messages=messages,
            # OpenRouter specific headers can be added here if needed
            extra_headers={
                "HTTP-Referer": "https://github.com/your-repo",
                "X-Title": "AI Divination App"
            }
        )
        
        complete_response = ""
        for event in ai_stream:
            if event.choices and event.choices[0].delta and event.choices[0].delta.content:
                current_response = event.choices[0].delta.content
                # 确保内容不为空且不重复
                if current_response and current_response.strip():
                    complete_response += current_response
                    # 发送响应数据和会话信息
                    response_data = {
                        "content": current_response,
                        "session_id": session_id,
                        "follow_up_count": session_manager.get_session(session_id).follow_up_count if session_id else 0,
                        "can_follow_up": session_manager.can_follow_up(session_id) if session_id else True
                    }
                    yield f"data: {json.dumps(response_data)}\n\n"
        
        # 将AI回复添加到会话
        if session_id and complete_response:
            session_manager.add_message(session_id, "assistant", complete_response)

    return StreamingResponse(get_ai_generator(), media_type='text/event-stream')
