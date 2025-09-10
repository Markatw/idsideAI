# package init (added in S21.5 protocol v2 consistency pass)

try:
    from .referrals import engine as referrals_engine
except Exception:
    referrals_engine = None
