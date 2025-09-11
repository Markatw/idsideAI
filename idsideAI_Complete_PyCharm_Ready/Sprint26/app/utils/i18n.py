"""
Sprint 24.6 — i18n hooks (protocol v2)
- t(key, lang) -> translated string
- set_lang(lang) / get_lang()
"""

import json
import os

from app.utils.perf import one_of as _one_of

_LANG = "en"


def set_lang(lang: str) -> str:
    global _LANG
    _LANG = _one_of(lang, ["en", "es", "fr", "de"], "en")
    return _LANG


def get_lang() -> str:
    return _LANG


def _dict_path(lang: str) -> str:
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root, "data", "i18n", f"{lang}.json")


def t(key: str, lang: str | None = None) -> str:
    if not key:
        return ""
    use = lang or get_lang()
    path = _dict_path(use)
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        d = {}
    return d.get(key, key)
