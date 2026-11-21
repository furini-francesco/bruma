from __future__ import annotations

from typing import Any


def get_health_status() -> dict[str, Any]:
    return {
        "status": "healthy",
        "service": "demo-api",
        "checks": {
            "database": "ok",
            "dependencies": "ok",
        },
    }
