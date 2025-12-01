def fetch_plan_options():
    """Return current pricing & plans."""
    return {
        "plans": [
            {"name": "Basic", "price": 9},
            {"name": "Pro", "price": 19},
            {"name": "Enterprise", "price": 49},
        ]
    }
