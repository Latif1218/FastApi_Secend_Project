from fastapi import APIRouter, Depends, status, HTTPException
from ..Authentication import user_auth
from sqlalchemy.orm import Session
from ..database import get_db



router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db), admin_user: Session = Depends(user_auth.get_current_user)):
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    if admin_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not enough permissions"
        )
    return db.query(user_auth.user_models.User).all()