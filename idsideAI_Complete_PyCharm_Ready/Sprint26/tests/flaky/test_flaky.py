"""
Sprint 26.8 — Flaky test demo (protocol v2)
"""
import random
from app.utils import flaky

def sometimes_passes():
    return random.random() > 0.5

def test_rerun_demo():
    res = flaky.rerun(sometimes_passes, times=5)
    assert isinstance(res, dict)
    print("Flaky rerun result:", res)
