from fastapi import HTTPException, status, APIRouter, Depends
from ..models import user_models
from ..schemas import user_schema
from sqlalchemy.orm import Session
from ..database import get_db
from ..Authentication.user_auth import get_current_user
from ..utils import hashing
from typing import Annotated

router = APIRouter(
    prefix="/Admin_regester"
)

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/users")
def get_users(db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Unauthorized"
        )
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Forbidden: Adnmin access required"
        )
    return db.query(user_models.User).all()