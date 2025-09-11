"""
Sprint 26.8 — Flaky test demo (protocol v2)
"""

import random
from app.utils import flaky


def sometimes_passes():
    return (
        random.random()
        > 0.5  # nosec B311 (low): vetted for board compliance - Standard pseudo-random generators are not suitable for security/cryptographic pu
    )  # nosec B311 (LOW): vetted for board compliance - Standard pseudo-random generators are not suitable for security/cryptographic pu


def test_rerun_demo():
    res = flaky.rerun(sometimes_passes, times=5)
    assert isinstance(
        res, dict
    )  # nosec B101 (LOW): vetted for board compliance - Use of assert detected. The enclosed code will be removed when compiling to opti
    print("Flaky rerun result:", res)
