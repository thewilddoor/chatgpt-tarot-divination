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


class OauthBody(BaseModel):
    login_type: str
    code: Optional[str]


class User(BaseModel):
    login_type: str
    user_name: str
    expire_at: float


class PlumFlower(BaseModel):
    num1: int
    num2: int


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


class DivinationBody(BaseModel):
    prompt: str
    prompt_type: str
    birthday: str
    plum_flower: Optional[PlumFlower] = None
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
