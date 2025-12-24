from fastapi import HTTPException, status, APIRouter, Depends
from ..models import user_models
from ..schemas import user_schema
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils import hashing
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from ..Authentication import user_auth
from datetime import timedelta


router = APIRouter(
    prefix="",
    tags=['Authentication']
)


@router.post("/token", response_model=user_schema.UserToken)
def login_user_access_token(
    user_credentials : Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(get_db),
):
    user = user_auth.authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "incorrect username and password",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    
    access_token = user_auth.create_access_token(
        data = {"user_id": user.id},
        expires_delta=timedelta(minutes=user_auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return user_schema.UserToken(access_token=access_token, token_type="bearer")


@router.get("/", status_code=status.HTTP_200_OK)
def user(user: Session = Depends(user_auth.get_current_user)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Faild"
        )
    return {"User": user}