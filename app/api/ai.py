from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database.mongodb import get_database
from app.api.auth import get_current_user
from app.services.gemini_service import analyze_incident_with_gemini
from app.services.rag_service import ask_security_question
from bson import ObjectId

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/analyze/{incident_id}")
async def analyze_incident(incident_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    incident = await db.incidents.find_one({"_id": ObjectId(incident_id)})
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    analysis_result = await analyze_incident_with_gemini(incident["description"])
    
    await db.incidents.update_one(
        {"_id": ObjectId(incident_id)},
        {"$set": {"ai_analysis": analysis_result}}
    )
    
    return {"message": "Analysis complete", "analysis": analysis_result}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    answer = ask_security_question(request.question)
    return ChatResponse(answer=answer)
