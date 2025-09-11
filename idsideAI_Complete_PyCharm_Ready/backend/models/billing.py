from typing import Literal

from pydantic import BaseModel

PlanTier = Literal["free", "starter", "pro", "enterprise"]


class Plan(BaseModel):
    id: str
    name: str
    tier: PlanTier
    price_cents: int
    currency: str = "USD"
    seats: int = 1
    features: list[str] = []


DEFAULT_PLANS = [
    Plan(
        id="free",
        name="Free",
        tier="free",
        price_cents=0,
        seats=3,
        features=["Basic graphs", "Exports (watermarked)"],
    ).dict(),
    Plan(
        id="starter",
        name="Starter",
        tier="starter",
        price_cents=990,
        seats=10,
        features=["Why export", "Audit export"],
    ),
    Plan(
        id="pro",
        name="Pro",
        tier="pro",
        price_cents=3990,
        seats=50,
        features=["Snapshots & Diff", "WebGL scaling", "Priority support"],
    ),
    Plan(
        id="enterprise",
        name="Enterprise",
        tier="enterprise",
        price_cents=14900,
        seats=200,
        features=["SAML SSO", "Dedicated support", "SLAs"],
    ),
]
