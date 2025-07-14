import json
import time
from typing import Optional
from types import SimpleNamespace
from fastapi.responses import StreamingResponse
from openai import OpenAI, APITimeoutError, APIConnectionError

import logging

logger = logging.getLogger(__name__)

from fastapi import Depends, HTTPException, Request, status


from src.config import settings
from fastapi import APIRouter

from src.models import DivinationBody, User
from src.user import get_user
from src.limiter import get_real_ipaddr, check_rate_limit
from src.divination import DivinationFactory
from src.session_manager import session_manager

client = OpenAI(
    api_key=settings.api_key, 
    base_url=settings.api_base,
    timeout=60.0  # 设置60秒超时
)
router = APIRouter()
_logger = logging.getLogger(__name__)
STOP_WORDS = [
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
            # 添加调试信息
            logger.warning(f"Session not found: {divination_body.session_id}")
            logger.warning(f"Current sessions: {list(session_manager.sessions.keys())}")
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
        temp_body = SimpleNamespace(
            prompt=original_divination.get("prompt", ""),
            prompt_type=original_prompt_type,
            birthday=original_divination.get("birthday", ""),
            plum_flower=None,
            tarot_draw_mode=original_divination.get("tarot_draw_mode", "random"),
            tarot_numbers=None,
            bazi=None
        )
        
        # 如果是梅花易数，重建plum_flower对象
        if original_prompt_type == "plum_flower" and original_divination.get("plum_flower"):
            plum_data = original_divination["plum_flower"]
            temp_body.plum_flower = SimpleNamespace(
                number=plum_data.get("number", "123456"),
                use_custom_time=plum_data.get("use_custom_time", False),
                custom_datetime=plum_data.get("custom_datetime", ""),
                model_dump=lambda: plum_data
            )
        
        # 如果是塔罗牌，重建tarot_numbers对象
        if original_prompt_type == "tarot" and original_divination.get("tarot_numbers"):
            tarot_data = original_divination["tarot_numbers"]
            temp_body.tarot_numbers = SimpleNamespace(
                first=tarot_data.get("first", 1),
                second=tarot_data.get("second", 2),
                third=tarot_data.get("third", 3)
            )
        
        # 如果是八字，重建bazi对象
        if original_prompt_type == "bazi" and original_divination.get("bazi"):
            bazi_data = original_divination["bazi"]
            temp_body.bazi = SimpleNamespace(
                birth_datetime=bazi_data.get("birth_datetime", "2000-08-17 10:30:00"),
                gender=bazi_data.get("gender", "male"),
                is_lunar=bazi_data.get("is_lunar", False),
                location=bazi_data.get("location", ""),
                model_dump=lambda: bazi_data
            )
        
        # 对塔罗牌类型特殊处理，追问时不重新抽牌
        if original_prompt_type == "tarot":
            # 塔罗牌追问时使用简化的提示，不重新抽牌
            from src.divination.tarot import TAROT_PROMPT
            original_full_prompt = f"您的问题：{original_divination.get('prompt', '')}\n\n（此为追问模式，使用之前抽取的塔罗牌结果）"
            system_prompt = TAROT_PROMPT
        else:
            # 其他占卜类型正常处理
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
            "plum_flower": divination_body.plum_flower.model_dump() if divination_body.plum_flower else None,
            "tarot_draw_mode": divination_body.tarot_draw_mode,
            "tarot_numbers": divination_body.tarot_numbers.model_dump() if divination_body.tarot_numbers else None,
            "bazi": divination_body.bazi.model_dump() if divination_body.bazi else None
        }
        session_id = session_manager.create_session(original_divination)
        logger.info(f"Created new session: {session_id}")

    # custom api key, model and base url support
    custom_base_url = request.headers.get("x-api-url")
    custom_api_key = request.headers.get("x-api-key")
    custom_api_model = request.headers.get("x-api-model")
    api_client = client
    
    # Get the appropriate model based on divination type
    if is_follow_up:
        # For follow-up requests, get the original divination type from session
        session = session_manager.get_session(divination_body.session_id)
        divination_type = session.original_divination.get("prompt_type", "tarot")
    else:
        # For first-time requests, get from the request body
        divination_type = divination_body.prompt_type
    
    api_model = custom_api_model if custom_api_model else settings.get_model_for_divination_type(divination_type)
    if custom_base_url and custom_api_key:
        api_client = OpenAI(api_key=custom_api_key, base_url=custom_base_url, timeout=60.0)
    elif custom_api_key:
        api_client = OpenAI(api_key=custom_api_key, base_url=settings.api_base, timeout=60.0)

    if not (settings.api_base or custom_base_url) or not (settings.api_key or custom_api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请设置 API KEY 和 API BASE URL"
        )

    def get_ai_generator():
        try:
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
            
            # 构建API请求参数
            api_params = {
                "model": api_model,
                "max_tokens": 8192,
                "temperature": 0.6,
                "stream": True,
                "messages": messages,
                # OpenRouter specific headers can be added here if needed
                "extra_headers": {
                    "HTTP-Referer": "https://github.com/your-repo",
                    "X-Title": "AI Divination App"
                }
            }
            
            # 对于支持推理的模型，添加推理参数到extra_body
            if (settings.enable_reasoning and 
                ("deepseek/deepseek-r1" in api_model.lower() or "r1" in api_model.lower())):
                api_params["extra_body"] = {"include_reasoning": True}
                _logger.info(f"Using reasoning model {api_model} with include_reasoning=True")
            
            _logger.debug(f"API request params: {api_params}")
            ai_stream = api_client.chat.completions.create(**api_params)
            
            complete_response = ""
            complete_reasoning = ""
            for event in ai_stream:
                if event.choices and event.choices[0].delta:
                    delta = event.choices[0].delta
                    current_response = ""
                    current_reasoning = ""
                    
                    # 调试：打印delta的所有属性（仅在有内容时）
                    if delta.content or any(hasattr(delta, field) for field in ['reasoning_content', 'reasoning', 'think']):
                        _logger.info(f"Delta attributes: {[attr for attr in dir(delta) if not attr.startswith('_')]}")
                        _logger.info(f"Delta content: {delta.content if delta.content else 'None'}")
                    
                    # 处理常规内容
                    if delta.content:
                        current_response = delta.content
                        if current_response and current_response.strip():
                            complete_response += current_response
                    
                    # 处理推理内容（尝试多种可能的字段名）
                    reasoning_fields = ['reasoning_content', 'reasoning', 'think']
                    for field in reasoning_fields:
                        if hasattr(delta, field):
                            reasoning_value = getattr(delta, field)
                            if reasoning_value:
                                _logger.info(f"Found reasoning content in field '{field}': {reasoning_value[:100]}...")
                                current_reasoning = reasoning_value
                                if current_reasoning and current_reasoning.strip():
                                    complete_reasoning += current_reasoning
                                break
                    
                    # 发送推理内容
                    if current_reasoning and current_reasoning.strip():
                        reasoning_data = {
                            "content": current_reasoning,
                            "content_type": "reasoning",
                            "session_id": session_id,
                            "follow_up_count": session_manager.get_session(session_id).follow_up_count if session_id else 0,
                            "can_follow_up": session_manager.can_follow_up(session_id) if session_id else True
                        }
                        yield f"data: {json.dumps(reasoning_data)}\n\n"
                    
                    # 发送常规响应数据和会话信息
                    if current_response and current_response.strip():
                        response_data = {
                            "content": current_response,
                            "content_type": "response",
                            "session_id": session_id,
                            "follow_up_count": session_manager.get_session(session_id).follow_up_count if session_id else 0,
                            "can_follow_up": session_manager.can_follow_up(session_id) if session_id else True
                        }
                        yield f"data: {json.dumps(response_data)}\n\n"
            
            # 如果有推理内容，将其添加到完整响应的开头
            if complete_reasoning:
                complete_response = f"<think>{complete_reasoning}</think>\n\n{complete_response}"
            
            # 将AI回复添加到会话
            if session_id and complete_response:
                session_manager.add_message(session_id, "assistant", complete_response)
                
        except APITimeoutError as e:
            _logger.error(f"API timeout error: {e}")
            error_data = {
                "content": "❌ 服务器响应超时，请稍后重试。这可能是由于网络延迟或API服务器负载过高造成的。",
                "session_id": session_id,
                "follow_up_count": session_manager.get_session(session_id).follow_up_count if session_id else 0,
                "can_follow_up": session_manager.can_follow_up(session_id) if session_id else True
            }
            yield f"data: {json.dumps(error_data)}\n\n"
        except APIConnectionError as e:
            _logger.error(f"API connection error: {e}")
            error_data = {
                "content": "❌ 网络连接失败，请检查网络设置后重试。",
                "session_id": session_id,
                "follow_up_count": session_manager.get_session(session_id).follow_up_count if session_id else 0,
                "can_follow_up": session_manager.can_follow_up(session_id) if session_id else True
            }
            yield f"data: {json.dumps(error_data)}\n\n"
        except Exception as e:
            _logger.error(f"Unexpected error: {e}")
            error_data = {
                "content": f"❌ 占卜过程中发生错误：{str(e)}",
                "session_id": session_id,
                "follow_up_count": session_manager.get_session(session_id).follow_up_count if session_id else 0,
                "can_follow_up": session_manager.can_follow_up(session_id) if session_id else True
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(get_ai_generator(), media_type='text/event-stream')
