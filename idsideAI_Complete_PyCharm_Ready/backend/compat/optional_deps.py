def optional_import(name, fallback=None):
    try:
        return __import__(name)
    except Exception:
        return fallback

stripe = optional_import("stripe", None)
prometheus_client = optional_import("prometheus_client", None)
neo4j = optional_import("neo4j", None)
