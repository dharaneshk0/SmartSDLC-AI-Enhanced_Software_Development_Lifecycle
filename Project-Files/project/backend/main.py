from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from routes import ai_routes, chat_routes, feedback_routes
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="SmartSDLC API",
    description="AI-Enhanced Software Development Lifecycle Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI Services"])
app.include_router(chat_routes.router, prefix="/api/chat", tags=["Chatbot"])
app.include_router(feedback_routes.router, prefix="/api/feedback", tags=["Feedback"])

@app.get("/")
async def root():
    return {"message": "SmartSDLC API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SmartSDLC API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)