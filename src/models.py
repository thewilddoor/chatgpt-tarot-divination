from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SettingsInfo(BaseModel):
    login_type: str
    user_name: str
    rate_limit: str
    user_rate_limit: str
    ad_client: str = ""
    ad_slot: str = ""
    enable_login: bool = False
    enable_rate_limit: bool = False



class User(BaseModel):
    login_type: str
    user_name: str
    expire_at: float


class PlumFlower(BaseModel):
    number: str = Field(min_length=1, max_length=32, description="起卦数字，将按位数分割", pattern=r'^\d+$')
    custom_datetime: Optional[str] = Field(None, description="自定义起卦时间，格式：YYYY-MM-DD HH:MM:SS")
    use_custom_time: bool = Field(False, description="是否使用自定义时间")


class TarotNumbers(BaseModel):
    first: int = Field(ge=1, le=78, description="第一张牌的位置(1-78)")
    second: int = Field(ge=1, le=78, description="第二张牌的位置(1-78)")
    third: int = Field(ge=1, le=78, description="第三张牌的位置(1-78)")


class Bazi(BaseModel):
    birth_datetime: str = Field(description="出生时间，格式：YYYY-MM-DD HH:MM:SS")
    gender: str = Field(default="male", description="性别，male或female")
    is_lunar: bool = Field(default=False, description="是否为农历")
    location: Optional[str] = Field(None, description="出生地点（可选，用于真太阳时修正）")


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: float


class DivinationSession(BaseModel):
    session_id: str
    original_divination: Dict[str, Any]  # 原始卦象信息
    messages: List[ChatMessage] = []
    follow_up_count: int = 0
    max_follow_ups: int = 10
    max_context_messages: int = 5
    created_at: float = 0.0  # 会话创建时间戳


class DivinationBody(BaseModel):
    prompt: str
    prompt_type: str
    birthday: Optional[str] = None
    plum_flower: Optional[PlumFlower] = None
    # 塔罗牌相关字段
    tarot_draw_mode: Optional[str] = Field(None, description="塔罗抽牌模式: random 或 numbers")
    tarot_numbers: Optional[TarotNumbers] = None
    # 八字相关字段
    bazi: Optional[Bazi] = None
    # 追问相关字段
    session_id: Optional[str] = None
    is_follow_up: bool = False
    follow_up_question: Optional[str] = None


class BirthdayBody(BaseModel):
    birthday: str = Field(example="2000-08-17 00:00:00")


class CommonResponse(BaseModel):
    content: str
    request_id: str


class DivinationResponse(BaseModel):
    content: str
    session_id: str
    follow_up_count: int
    can_follow_up: bool
    original_divination_summary: Optional[str] = None
