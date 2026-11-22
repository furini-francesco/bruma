# legge YAML, valida lo schema e stampa errori comprensibili.
## esempio utilizzo comando iniziale: python platform/validator/validate_workload.py platform/examples/demo-api-local.yaml

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

# lettura file YAML
def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError("Il file YAML deve contenere un oggetto.")

    return data

# lettura schema JSON
def load_schema(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        schema = json.load(file)

    return schema

# verifica YAML rispetti lo schema
def format_location(error: ValidationError) -> str:
    location = ".".join(str(part) for part in error.absolute_path)

    return location or "<radice>"

def validate_workload(
    workload: dict[str, Any],
    schema: dict[str, Any],
) -> list[ValidationError]:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise ValueError(
            f"Lo schema JSON non è valido: {error.message}"
        ) from error

    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(workload),
        key=lambda error: list(error.absolute_path),
    )

    return errors

# mostrare risultati o errori
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un Workload YAML contro lo schema Bruma."
    )
    parser.add_argument(
        "workload",
        type=Path,
        help="Percorso del file Workload YAML",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "schema"
        / "workload.schema.json",
        help="Percorso dello schema JSON",
    )

    arguments = parser.parse_args()

    try:
        workload = load_yaml(arguments.workload)
        schema = load_schema(arguments.schema)
        errors = validate_workload(workload, schema)
    except (OSError, yaml.YAMLError, json.JSONDecodeError, ValueError) as error:
        print(f"Errore: {error}", file=sys.stderr)
        return 1

    if errors:
        print(
            f"Workload non valido: {arguments.workload}",
            file=sys.stderr,
        )

        for error in errors:
            location = format_location(error)
            print(f"- {location}: {error.message}", file=sys.stderr)

        return 1

    print(f"Workload valido: {arguments.workload}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())