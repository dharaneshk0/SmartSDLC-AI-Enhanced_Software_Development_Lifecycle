from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from datetime import datetime

router = APIRouter()

class FeedbackRequest(BaseModel):
    feature: str
    rating: int
    comment: Optional[str] = None
    user_id: Optional[str] = None

class FeedbackResponse(BaseModel):
    success: bool
    message: str

# Simple file-based storage for feedback
FEEDBACK_FILE = "feedback_data.json"

def load_feedback():
    try:
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'r') as f:
                return json.load(f)
        return []
    except:
        return []

def save_feedback(feedback_list):
    try:
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(feedback_list, f, indent=2)
        return True
    except:
        return False

@router.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    try:
        feedback_list = load_feedback()
        
        new_feedback = {
            "feature": request.feature,
            "rating": request.rating,
            "comment": request.comment,
            "user_id": request.user_id,
            "timestamp": datetime.now().isoformat()
        }
        
        feedback_list.append(new_feedback)
        
        if save_feedback(feedback_list):
            return FeedbackResponse(
                success=True,
                message="Feedback submitted successfully"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save feedback")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")

@router.get("/stats")
async def get_feedback_stats():
    try:
        feedback_list = load_feedback()
        
        if not feedback_list:
            return {"total_feedback": 0, "average_rating": 0, "features": {}}
        
        total_feedback = len(feedback_list)
        total_rating = sum(f.get("rating", 0) for f in feedback_list)
        average_rating = total_rating / total_feedback if total_feedback > 0 else 0
        
        # Group by feature
        features = {}
        for feedback in feedback_list:
            feature = feedback.get("feature", "unknown")
            if feature not in features:
                features[feature] = {"count": 0, "ratings": []}
            features[feature]["count"] += 1
            features[feature]["ratings"].append(feedback.get("rating", 0))
        
        # Calculate average rating per feature
        for feature in features:
            ratings = features[feature]["ratings"]
            features[feature]["average_rating"] = sum(ratings) / len(ratings) if ratings else 0
        
        return {
            "total_feedback": total_feedback,
            "average_rating": round(average_rating, 2),
            "features": features
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting feedback stats: {str(e)}")