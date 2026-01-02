import sys
import os
import asyncio

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.shared.core.config import settings
from src.shared.core.logging import logger, configure_logging
from src.shared.core.security import create_access_token, get_password_hash, verify_password
from src.shared.ai.client import ai_client

configure_logging()

async def main():
    logger.info("VERIFICATION_START", project=settings.PROJECT_NAME)
    
    # Check Config
    if settings.DATABASE_URL:
        logger.info("CONFIG_CHECK_PASS", db_url_present=True)
    else:
        logger.error("CONFIG_CHECK_FAIL")

    # Check Security
    pwd = "secret"
    hashed = get_password_hash(pwd)
    valid = verify_password(pwd, hashed)
    token = create_access_token("test_user")
    
    if valid and token:
        logger.info("SECURITY_CHECK_PASS", token_generated=True)
    else:
        logger.error("SECURITY_CHECK_FAIL")

    # Check AI Client (Mock)
    response = await ai_client.get_chat_completion([{"role": "user", "content": "Hello"}])
    logger.info("AI_CHECK_PASS", response=response)

    logger.info("VERIFICATION_COMPLETE")

if __name__ == "__main__":
    asyncio.run(main())
