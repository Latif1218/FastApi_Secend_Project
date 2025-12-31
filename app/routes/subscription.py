from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import user_models, user_subscription_models
from ..schemas import user_subscription_schema
from ..database import get_db
from ..Authentication import user_auth
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/subscriptions", 
    tags=["Subscriptions"]
)


@router.get("/me", response_model=user_subscription_schema.SubscriptionOut)
def get_my_sebscription(
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    sub = db.query(user_subscription_models.Subscription).filter(
        user_subscription_models.Subscription.user_id == user.id
    ).first()
    
    if not sub:
        sub = user_subscription_models.Subscription(
            id = None,
            user_id = user.id,
            plan = "free",
            status = "active",
            started_at = datetime.utcnow(),
            ends_at = None
        )
        
    return sub



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_subscription_schema.SubscriptionOut)
def create_or_update_subscription(
    payload: user_subscription_schema.SubscriptionCreate,
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    sub = db.query(user_subscription_models.Subscription).filter(
        user_subscription_models.Subscription.user_id == user.id 
    ).first()
    
    if sub: 
        sub.plan = payload.plan
        sub.status = "active"
        sub.payment_provider = payload.payment_provider
        sub.payment_id = payload.payment_id
    else:
        sub = user_subscription_models.Subscription(
            user_id = user.id,
            plan = payload.plan,
            payload_provider = payload.payment_provider,
            payment_id = payload.payment_id
        )
        db.add(sub)
        
        
    if payload.plan == "monthly":
        sub.ends_at = datetime.utcnow() + timedelta(days=30)
    elif payload.plan == "yearly":
        sub.ends_at = datetime.utcnow() + timedelta(days=365)
        
        
    user.is_premium = (payload.plan != "free")
    
    db.commit()
    db.refresh(sub)
    
    return sub



@router.post("/cancel", status_code=status.HTTP_200_OK)
def cancel_subscription(
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_auth.get_current_user)
):
    sub = db.query(user_subscription_models.Subscription).filter(
        user_subscription_models.Subscription.user_id == user.id
    ).first()
    
    if not sub or sub.plan == "free":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription to cancel"
        )
        
    sub.status = "canceled"
    user.is_premium = False
    
    db.commit()
    
    return {"massage": "Subscriptions candeled successfully. premium fertures will remain until end of builling period"}