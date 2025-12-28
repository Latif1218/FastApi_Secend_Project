from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models import user_models, user_mood_models, user_habit_models
from ..schemas import user_schema, user_mood_schema, user_habit_schema
from ..Authentication import user_auth
from ..database import get_db
from datetime import date



router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_habit_schema.HabitOut)
def create_habit(
    payload: user_habit_schema.HabitCreate,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user) 
):
    new_habit = user_habit_models.Habit(
        name=payload.name,
        description=payload.description,
        category=payload.category,
        frequency=payload.frequency,
        reminder_time=payload.reminder_time,
        user_id = user.id
    )
    
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit




@router.get("/", status_code=status.HTTP_200_OK, response_model= List[user_habit_schema.HabitOut])
def get_my_habits(
    db:Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    return db.query(user_habit_models.Habit).filter(
        user_habit_models.Habit.user_id == user.id
    ).all()
    
    
    
@router.patch("/{habit_id}", status_code=status.HTTP_200_OK, response_model=user_habit_schema.HabitOut)
def update_habit(
    habit_id: int,
    update_data: user_habit_schema.HabitUpdate,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    habit = db.query(user_habit_models.Habit).filter(
        user_habit_models.Habit.id == habit_id,
        user_habit_models.Habit.user_id == user.id 
    ).first()
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit is not found"
        )
        
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(habit, key, value)
            
    db.commit()
    db.refresh(habit)
    return habit




@router.delete("/{habit_id}", status_code=status.HTTP_200_OK)
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    habit = db.query(user_habit_models.Habit).filter(
        user_habit_models.Habit.id == habit_id,
        user_habit_models.Habit.user_id == user.id
    ).first()
    
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="habit is not found"
        )
    db.delete(habit)
    db.commit()
    return {"massage": "Habit deleted successfully"}    