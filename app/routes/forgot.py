from fastapi import APIRouter, Depends, status, HTTPException
from ..Authentication import user_auth
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import user_schema
from ..models import user_models
from ..utils.otp_sender import generate_otp
from ..utils.email_sender import send_otp_email
from datetime import datetime, timedelta, timezone



router = APIRouter(
    prefix="/forgot",
    tags=["Forgot Password"]
)


@router.post("/forgot_pass", status_code=status.HTTP_200_OK)
def forgot_password(payload: user_schema.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email dose not esist"
        )
    set_otp = generate_otp()
    db.query(user_models.PasswordResetCode).filter(
        user_models.PasswordResetCode.user_id == user.id,
        user_models.PasswordResetCode.used == False
    ).delete()
    
    otp_record = user_models.PasswordResetCode(
        user_id = user.id,
        code = set_otp,
        used = False,
        Expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    db.add(otp_record)
    db.commit()
    
    sent = send_otp_email(to_email = user.email, otp = set_otp)
    
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send otp email"
        )
    return {
        "status": "success",
        "message": f"password reset otp sent to {user.email}"
    }
    
    
    

@router.post("/verify_otp",status_code=status.HTTP_200_OK)
def verify_otp(payload: user_schema.OTPVerify, db: Session = Depends(get_db)):
    
    
    
    
    

