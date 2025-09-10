import json
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import os, stripe

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY","")

class Plan(BaseModel):
    id: str
    name: str
    price_id: str
    currency: str = "usd"
    interval: str = "month"
    amount: int | None = None

def _plans():
    return [
        {"id":"free","name":"Free","price_id": os.getenv("STRIPE_PRICE_FREE","price_free"), "amount":0},
        {"id":"starter","name":"Starter","price_id": os.getenv("STRIPE_PRICE_STARTER","price_starter"), "amount": 1900},
        {"id":"pro","name":"Pro","price_id": os.getenv("STRIPE_PRICE_PRO","price_pro"), "amount": 4900},
        {"id":"enterprise","name":"Enterprise","price_id": os.getenv("STRIPE_PRICE_ENTERPRISE","price_enterprise"), "amount": 0},
    ]

@router.get("/plans")
def get_plans():
    return {"plans": _plans(), "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY","")}

@router.post("/checkout")
async def checkout(request: Request):
    body = await request.json()
    price_id = body.get("price_id")
    success_url = body.get("success_url") or body.get("successUrl") or "http://localhost:5173?checkout=success"
    cancel_url = body.get("cancel_url") or body.get("cancelUrl") or "http://localhost:5173?checkout=cancel"
    # Optional: tenant id via header
    tenant = request.headers.get("X-Tenant","demo")
    if not stripe.api_key:
        # stub
        return {"url": success_url + "&stub=true"}
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"tenant": tenant}
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/portal")
async def portal(request: Request):
    body = await request.json()
    customer_id = body.get("customer_id") or body.get("customerId")
    return_url = body.get("return_url") or body.get("returnUrl") or "http://localhost:5173"
    if not stripe.api_key:
        return {"url": return_url + "?portal=stub"}
    if not customer_id:
        raise HTTPException(status_code=400, detail="customer_id required")
    try:
        portal = stripe.billing_portal.Session.create(customer=customer_id, return_url=return_url)
        return {"url": portal.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhooks/stripe")
async def webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET","")
    if webhook_secret and sig:
        try:
            event = stripe.Webhook.construct_event(payload=payload, sig_header=sig, secret=webhook_secret)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")
    else:
        # skip verify for local
        try:
            event = stripe.Event.construct_from(json.loads(payload or b"{}"), stripe.api_key)
        except Exception:
            event = {"type":"unknown"}

    # Handle events (minimal)
    et = event.get("type") if isinstance(event, dict) else getattr(event,"type", "unknown")
    # TODO: Update tenant plan in Neo4j based on checkout.session.completed or customer.subscription.updated
    return {"received": True, "type": et}
