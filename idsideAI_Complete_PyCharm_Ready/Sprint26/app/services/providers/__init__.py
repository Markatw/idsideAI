# package init (added in S21.5 protocol v2 consistency pass)

try:
    from app.services.payments import stripe_live
except Exception:
    stripe_live = None
