import json
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models import AnalysisResult, UserProfile
from ...shared.ai.client import ai_client
from ..api.schemas import AnalysisRequest

DISCLAIMER_TEXT = "\n\nDISCLAIMER: This is an AI-generated educational analysis. It is not financial advice. Consult a professional."

async def run_finance_analysis(
    user_id: str, 
    request: AnalysisRequest, 
    profile: UserProfile,
    db: AsyncSession
) -> AnalysisResult:
    
    # Construct Prompt
    profile_context = f"Risk Profile: {profile.risk_level}. Goals: {profile.goals}. Currency: {profile.currency}."
    user_prompt = f"{profile_context}\nUser Context: {request.context}\nData: {json.dumps(request.inputs)}"
    
    messages = [
        {"role": "system", "content": "You are MoneyPilot, an educational finance assistant. Provide general insights based on principles. Do NOT give specific investment advice."},
        {"role": "user", "content": user_prompt}
    ]
    
    # Call AI
    ai_response = await ai_client.get_chat_completion(messages, request_id=f"user-{user_id}")
    
    # Append Disclaimer
    final_output = ai_response + DISCLAIMER_TEXT
    
    # Audit / Persist
    result = AnalysisResult(
        user_id=user_id,
        summary=final_output,
        details=request.inputs, # Storing inputs as details for checking later
        disclaimer_version="v1"
    )
    
    db.add(result)
    await db.commit()
    await db.refresh(result)
    
    return result
