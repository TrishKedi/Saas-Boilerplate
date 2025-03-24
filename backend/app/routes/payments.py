import os
import stripe
from fastapi import APIRouter, HTTPException, Depends, Request
from dotenv import load_dotenv
from database import get_db
from models.user import User
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from auth import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # ❌ Wrong import


load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

if not STRIPE_SECRET_KEY:
    raise ValueError("STRIPE_SECRET_KEY is not set in environment variables")

stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter(prefix="/payments", tags=["payments"])
current_active_user = fastapi_users.current_user(active=True)

@router.post("/create-customer")
async def create_customer(
    db: AsyncSession = Depends(get_db),  # ✅ Get the correct async session
    user: User = Depends(current_active_user),  # ✅ Get authenticated user
):

    try:
        # ✅ Ensure user is retrieved properly from DB
        stmt = select(User).where(User.id == user.id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.stripe_customer_id:
            return {"message": "User already has a Stripe customer ID", "customer_id": user.stripe_customer_id}

        # ✅ Create Stripe Customer
        customer = stripe.Customer.create(
            email=user.email,
            metadata={"user_id": str(user.id)}
        )

        # ✅ Store Stripe Customer ID in DB
        user.stripe_customer_id = customer.id
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return {"customer_id": customer.id}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ Create Checkout Session for Subscription
@router.post("/create-checkout-session")
def create_checkout_session(request: Request, db: Session = Depends(get_db), user: User = Depends(current_active_user)):
    #  return {"message": "User authenticated", "user_email": user.email, "stripe_customer_id": user.stripe_customer_id}
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=user.stripe_customer_id,
            line_items=[
                {
                    "price": "price_1R69OQIqC56fhixKg2VfH2Vw",  # Replace with actual Stripe price ID
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=f"{request.base_url}payments/success",
            cancel_url=f"{request.base_url}payments/cancel",
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Webhook to Handle Stripe Events
@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
    # ✅ Handle subscription activation
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session["customer"]
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_status = "active"
            db.commit()

    # ✅ Handle failed payments
    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        customer_id = invoice["customer"]
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_status = "past_due"
            db.commit()
    
    return {"status": "success"}

# ✅ Check Subscription Status
@router.get("/subscription-status")
def get_subscription_status(user: User = Depends(), db: Session = Depends(get_db)):
    if not user.stripe_customer_id:
        return {"subscription_status": "inactive"}
    
    try:
        subscriptions = stripe.Subscription.list(customer=user.stripe_customer_id, status="active")
        if subscriptions["data"]:
            return {"subscription_status": "active"}
        return {"subscription_status": "inactive"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Cancel Subscription
@router.post("/cancel-subscription")
def cancel_subscription(user: User = Depends(), db: Session = Depends(get_db)):
    if not user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="User does not have a subscription")
    
    try:
        subscriptions = stripe.Subscription.list(customer=user.stripe_customer_id, status="active")
        if not subscriptions["data"]:
            raise HTTPException(status_code=400, detail="No active subscriptions found")
        
        subscription_id = subscriptions["data"][0]["id"]
        stripe.Subscription.delete(subscription_id)
        
        user.subscription_status = "canceled"
        db.commit()
        return {"message": "Subscription canceled successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
