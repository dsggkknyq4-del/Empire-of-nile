from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
# We need a User model to validate existence. 
# Ideally we should have a 'SharedUser' model in shared/db/models.py 
# but for this MVP we used MoneyPilot's user.
# To keep TongueForge independent, we will assume it shares the SAME DB/Auth 
# and we can define a minimal User mapping or just trust the JWT payload for ID.
# For robustness, let's duplicate the User model check against the TABLE 'mp_users' 
# or introduce a 'shared_users' table. 
# Given the Monorepo instruction "can be mono-repo or 3 repos", and MoneyPilot already owns the users...
# Let's assume TongueForge uses its own Users or Shared Users.
# PHASE 0 said "Role model (user/admin)" in shared foundation but we put it in MoneyPilot.
# CORRECTION: I will rely on JWT sub (user_id) without DB check for MVP speed in TongueForge,
# OR query the `mp_users` table if they share the same DB instance (which they do in docker-compose).

from ...shared.core.config import settings
from ...shared.db.base import get_db_session
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/moneypilot/auth/login") # Pointing to MP auth for now or generic

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> uuid.UUID:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        return uuid.UUID(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception
