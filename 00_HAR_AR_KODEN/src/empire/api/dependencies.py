from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import uuid
from typing import Optional

from ...shared.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/moneypilot/auth/login", auto_error=False)

async def get_optional_user_id(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[uuid.UUID]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str:
            return uuid.UUID(user_id_str)
    except (JWTError, ValueError):
        pass # Return None if invalid
    return None
