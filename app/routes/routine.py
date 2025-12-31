from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..models import user_models, user_routine_models, user_mood_models
from ..schemas import user_routine_schema, user_mood_schema
from ..database import get_db
from ..Authentication import user_auth
from ..utils.ai_routine_generator import genarate_ai_routine



router = APIRouter(
    prefix="/routines",
    tags=["Routines"]
)

# create routine

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_routine_schema.RoutineOut)
def generate_ai_personalized_routine(
    mood_data: user_mood_schema.MoodCreate,
    preferred_time: str | None = None,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    """
    AI uses latest mood to generate a personalized routine
    """
    
    ai_response = genarate_ai_routine(
        mood_rating=mood_data.rating,
        emotions=mood_data.emotions,
        note=mood_data.note,
        preferred_time=preferred_time
    )
    
    new_routine = user_routine_models.Routine(
        name=ai_response["name"],
        duration_minutes=ai_response["duration_minutes"],
        is_ai_generated=True,
        scheduled_time=ai_response.get("scheduled_time"),
        user_id=user.id
    )
    db.add(new_routine)
    db.flush()
    
    for act in ai_response["activities"]:
        activity = user_routine_models.RoutineActivity(
            routine_id=new_routine.id,
            activity_type=act["activity_type"],
            title=act["title"],
            duration_minutes=act["duration_minutes"]
        )
        db.add(activity)
        
    db.commit()
    db.refresh(new_routine)
    
    return new_routine



# my rootin list

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[user_routine_schema.RoutineOut])
def get_my_routines(
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    routines = db.query(user_routine_models.Routine).filter(
        user_routine_models.Routine.user_id == user.id
    ).order_by(user_routine_models.Routine.created_at.desc()).all()
    
    return routines