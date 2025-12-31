from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime as dt
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



# get todays routine

@router.get("/today", status_code=status.HTTP_200_OK, response_model=List[user_routine_schema.RoutineOut])
def get_today_routines(
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    
    today = date.today()
    routines = db.query(user_routine_models.Routine).filter(
        user_routine_models.Routine.user_id == user.id
    ).filter(
        user_routine_models.Routine.created_at >= dt.combine(today, dt.min.time())
    ).filter(
        user_routine_models.Routine.created_at < dt.combine(today, dt.max.time())
    ).order_by(
        user_routine_models.Routine.is_ai_generated.desc()
    ).all()
    
    return routines




# marked router completed

@router.patch("/{routine_id}/complete", status_code=status.HTTP_200_OK, response_model=user_routine_schema.RoutineOut)
def complete_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    routine = db.query(user_routine_models.Routine).filter(
        user_routine_models.Routine.id == routine_id
    ).filter(
        user_routine_models.Routine.user_id == user.id
    ).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
        
    if routine.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Routine already compleated"
        )
        
    routine.completed = True
    routine.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(routine)
    return routine




# Do it again Routin duplicate

@router.post("/{routine_id}/redo", status_code=status.HTTP_201_CREATED, response_model=user_routine_schema.RoutineOut)
def redo_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    original = db.query(user_routine_models.Routine).filter(
        user_routine_models.Routine.id == routine_id
    ).filter(
        user_routine_models.Routine.user_id == user.id
    ).first()
    
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
        
    new_routine = user_routine_models.Routine(
        name = original.name + " (Again)",
        duration_minutes = original.duration_minutes,
        is_ai_generated=original.is_ai_generated,
        scheduled_time=original.scheduled_time,
        user_id=user.id,
        completed=False
    )
    
    db.add(new_routine)
    db.flush()
    
    for act in original.activities:
        new_act = user_routine_models.RoutineActivity(
            routine_id=new_routine.id,
            activity_type=act.activity_type,
            title=act.title,
            duration_minutes=act.duration_minutes
        )
        
        db.add(new_act)
        
    db.commit()
    db.refresh(new_routine)
    return new_routine




# routin Deleted

@router.delete("/{router_id}")
def delete_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    routine = db.query(user_routine_models.Routine).filter(
        user_routine_models.Routine.id == routine_id
    ).filter(
        user_routine_models.Routine.user_id == user.id
    ).first()
    
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
        
    db.delete(routine)
    db.commit()
    return {"massage": "Routine deleted successfully"}

