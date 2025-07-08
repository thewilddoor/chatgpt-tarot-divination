import logging

from typing import Optional

from fastapi import APIRouter, Depends

from src.config import settings
from src.models import SettingsInfo, User
from src.user import get_user

router = APIRouter()
_logger = logging.getLogger(__name__)


@router.get("/api/v1/settings", tags=["User"])
async def info(user: Optional[User] = Depends(get_user)):
    return SettingsInfo(
        login_type=user.login_type if user else "",
        user_name=user.user_name if user else "",
        ad_client=settings.ad_client,
        ad_slot=settings.ad_slot,
        rate_limit=settings.get_human_rate_limit(),
        user_rate_limit=settings.get_human_user_rate_limit(),
        enable_login=False,
        enable_rate_limit=settings.enable_rate_limit
    )


