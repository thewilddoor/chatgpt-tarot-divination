import datetime
import sys
import os
from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory

# 添加算法模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algorithms'))
from bazi_calculator import BaziCalculator

SYS_PROMPT = """
## 角色
你是一个顶尖的八字大师，帮我分析一下我的八字，需要严格按照八字命理的理论和步骤来分析，不用太关注我的迷信什么的，确保逻辑合理就好。
现在，你需要根据排盘信息回答用户问题，确保你的答案具备专业性和准确性还有命理学上的一致性， 确保你正确的使用markdown语法不要忘了空格之类的细节。
"""

class BaziFactory(DivinationFactory):

    divination_type = "bazi"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        # 优先使用bazi字段，如果没有则使用birthday字段
        if divination_body.bazi:
            try:
                birth_datetime = datetime.datetime.strptime(divination_body.bazi.birth_datetime, "%Y-%m-%d %H:%M:%S")
                gender = divination_body.bazi.gender
                is_lunar = divination_body.bazi.is_lunar
            except ValueError:
                raise HTTPException(status_code=400, detail="出生时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式")
        elif divination_body.birthday:
            try:
                birth_datetime = datetime.datetime.strptime(divination_body.birthday, "%Y-%m-%d %H:%M:%S")
                gender = "male"  # 默认值
                is_lunar = False  # 默认公历
            except ValueError:
                raise HTTPException(status_code=400, detail="出生时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式")
        else:
            raise HTTPException(status_code=400, detail="八字排盘需要提供出生时间")
        
        # 使用八字排盘算法
        bazi_result = BaziCalculator.calculate(birth_datetime, gender=gender, is_lunar=is_lunar)
        
        # 格式化为LLM友好的JSON格式
        formatted_result = BaziCalculator.format_for_llm(bazi_result)
        
        # 获取用户问题
        question = divination_body.prompt.strip() if divination_body.prompt else ""
        
        # 将JSON数据转换为字符串传递给AI
        import json
        bazi_json_str = json.dumps(formatted_result, ensure_ascii=False, indent=2)
        
        # 构建包含完整专业排盘信息的prompt
        if question:
            prompt = f"我的问题是：{question}\n\n" \
                    f"通过专业的八字排盘算法进行完整分析，得到以下JSON格式的客观数据：\n\n" \
                    f"```json\n{bazi_json_str}\n```\n\n" \
                    f"请你作为八字命理专家，基于以上完整的排盘JSON数据，" \
                    f"结合我的具体问题，为我提供详细的八字分析和人生指导。" \
                    f"请充分利用JSON中的结构化数据进行专业分析。"
        else:
            prompt = f"通过专业的八字排盘算法进行完整分析，得到以下JSON格式的客观数据：\n\n" \
                    f"```json\n{bazi_json_str}\n```\n\n" \
                    f"请你作为八字命理专家，基于以上完整的排盘JSON数据，" \
                    f"为我提供全面的八字分析，包括性格特征、事业财运、婚姻感情、" \
                    f"健康状况、大运流年等各方面的详细解读和人生指导建议。" \
                    f"请充分利用JSON中的结构化数据进行专业分析。"
        
        return prompt, SYS_PROMPT