from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from demo_api.health import get_health_status


def test_health_status_is_healthy() -> None:
    health = get_health_status()

    assert health["status"] == "healthy"
    assert health["service"] == "demo-api"
    assert health["checks"]["database"] == "ok"
