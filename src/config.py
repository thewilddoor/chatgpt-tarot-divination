import logging
from typing import Tuple

from pydantic import Field
from pydantic_settings import BaseSettings

_logger = logging.getLogger(__name__)


class Settings(BaseSettings):

    # project settings
    project_name: str = "ai-divination"

    # OpenRouter API settings
    api_key: str = Field(default="", exclude=True, alias="API_KEY")
    api_base: str = Field(default="https://openrouter.ai/api/v1", alias="API_BASE")
    model: str = Field(default="anthropic/claude-sonnet-4", alias="MODEL")
    
    # Individual model settings for each divination type
    bazi_model: str = Field(default="deepseek/deepseek-r1-0528", alias="BAZI_MODEL")
    tarot_model: str = Field(default="anthropic/claude-sonnet-4", alias="TAROT_MODEL")
    dream_model: str = Field(default="anthropic/claude-sonnet-4", alias="DREAM_MODEL")
    plum_flower_model: str = Field(default="anthropic/claude-sonnet-4", alias="PLUM_FLOWER_MODEL")
    birthday_model: str = Field(default="anthropic/claude-sonnet-4", alias="BIRTHDAY_MODEL")
    
    # Reasoning functionality settings
    enable_reasoning: bool = Field(default=True, alias="ENABLE_REASONING")


    # google ads settings
    ad_client: str = Field(default="", alias="AD_CLIENT")
    ad_slot: str = Field(default="", alias="AD_SLOT")

    # cache settings
    cache_client_type: str = Field(default="memory", alias="CACHE_CLIENT_TYPE")
    redis_url: str = Field(default="", exclude=True, alias="KV_URL")
    upstash_api_url: str = Field(default="", alias="KV_REST_API_URL")
    upstash_api_token: str = Field(default="", exclude=True, alias="KV_REST_API_TOKEN")

    # rate limit settings
    enable_rate_limit: bool = Field(default=True, alias="ENABLE_RATE_LIMIT")
    # rate limit xxx request per xx seconds
    rate_limit: Tuple[int, int] = (60, 60 * 60)
    user_rate_limit: Tuple[int, int] = (600, 60 * 60)

    def get_human_rate_limit(self) -> str:
        max_reqs, time_window_seconds = self.rate_limit
        # convert to human readable format
        return f"{max_reqs}req/{time_window_seconds}seconds"

    def get_human_user_rate_limit(self) -> str:
        max_reqs, time_window_seconds = self.user_rate_limit
        # convert to human readable format
        return f"{max_reqs}req/{time_window_seconds}seconds"
    
    def get_model_for_divination_type(self, divination_type: str) -> str:
        """Get the appropriate model for the given divination type"""
        model_map = {
            "bazi": self.bazi_model,
            "tarot": self.tarot_model,
            "dream": self.dream_model,
            "plum_flower": self.plum_flower_model,
            "birthday": self.birthday_model
        }
        return model_map.get(divination_type, self.model)

    class Config:
        env_file = ".env"


settings = Settings()
