from __future__ import annotations

from typing import Any

from .health import get_health_status


def create_app() -> dict[str, Any]:
    return {
        "name": "bruma-demo-api",
        "status": "ok",
        "version": "0.1.0",
        "health": get_health_status(),
    }


def main() -> None:
    print(create_app())


if __name__ == "__main__":
    main()
