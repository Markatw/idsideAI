"""
Sprint 28.4 — Stripe live integration scaffold (protocol v2)
Reads STRIPE_SECRET_KEY from env and configures client if available.
"""
import os

try:
    import stripe
except ImportError:
    stripe = None

class StripeLiveClient:
    def __init__(self):
        key = os.getenv("STRIPE_SECRET_KEY")
        if not key:
            raise RuntimeError("STRIPE_SECRET_KEY not set")
        if stripe is None:
            raise RuntimeError("stripe library not installed")
        stripe.api_key = key

    def verify_key(self):
        # Lightweight check (does not call API in this scaffold)
        return bool(stripe.api_key)
