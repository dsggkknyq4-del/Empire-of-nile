from typing import List, Dict, Optional, Any
from openai import AsyncOpenAI
from .config import settings
from .logging import logger

class AIClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        self.model = settings.AI_MODEL

    async def get_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 500,
        request_id: Optional[str] = None
    ) -> str:
        """
        Wrapper for AI calls to enforce logging and potential future constraints.
        """
        log = logger.bind(request_id=request_id)
        
        if not self.client:
            log.warning("AI_CLIENT_MISSING_KEY", message="OpenAI API key not set. Returning mock response.")
            return "[MOCK AI RESPONSE] AI key is missing. Please configure OPENAI_API_KEY."

        # Redact sensitive info in logs if needed (simple placeholder for now)
        log.info("AI_REQUEST_START", model=self.model, message_count=len(messages))

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            
            # Enforce server-side disclaimer if strictly needed in the raw text, 
            # though usually better to append in application logic. 
            # We will log the size but not the full content to avoid PII retention unless debug.
            log.info("AI_REQUEST_SUCCESS", response_chars=len(content))
            
            return content

        except Exception as e:
            log.error("AI_REQUEST_FAILED", error=str(e))
            raise e

# Global instance
ai_client = AIClient()
