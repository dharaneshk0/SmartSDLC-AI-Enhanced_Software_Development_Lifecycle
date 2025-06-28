from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.watsonx_service import watsonx_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    success: bool

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = watsonx_service.chat_response(request.message)
        
        return ChatResponse(
            response=response,
            success=True
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@router.get("/chat/health")
async def chat_health():
    return {"status": "healthy", "service": "chatbot"}