from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models import user_models, user_mood_models
from ..schemas import user_mood_schema, user_schema
from ..database import get_db
from ..Authentication import user_auth




router = APIRouter(
    prefix="/moods",
    tags=["Moods"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_mood_schema.MoodCreate)
def create_mood(
    payload : user_mood_schema.MoodCreate,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    new_mood = user_mood_models.Mood(
        user_id = user.id,
        rating=payload.rating,
        emotions=payload.emotions,
        note=payload.note
    )
    
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)
    return new_mood




@router.get("/", status_code=status.HTTP_200_OK, response_model=List[user_mood_schema.MoodOut])
def get_my_moods(
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    return db.query(user_mood_models.Mood).filter(
        user_mood_models.Mood.user_id==user.id
    ).order_by(
        user_mood_models.Mood.created_at.desc()
    ).all()




@router.get("/history", status_code=status.HTTP_200_OK, response_model=list[user_mood_schema.MoodOut])
def get_mood_history(
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    return db.query(user_mood_models.Mood).filter(
        user_mood_models.Mood.user_id==user.id
    ).order_by(
        user_mood_models.Mood.created_at.desc()
    ).limit(30).all()