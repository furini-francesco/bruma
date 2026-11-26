import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from validate_workload import (
    format_location,
    load_schema,
    load_yaml,
    validate_workload,
)


def split_image(image: str) -> tuple[str, str]:
    if "@" in image:
        raise ValueError(
            "Le immagini indicate con digest non sono ancora supportate "
            "dal chart: usa un tag, ad esempio repository:tag."
        )

    if any(character.isspace() for character in image):
        raise ValueError("Il riferimento dell'immagine contiene spazi.")

    last_slash = image.rfind("/")
    last_colon = image.rfind(":")

    if last_colon > last_slash:
        repository = image[:last_colon]
        tag = image[last_colon + 1 :]
    else:
        repository = image
        tag = "latest"

    if not repository or not tag:
        raise ValueError(f"Riferimento dell'immagine non valido: {image!r}")

    return repository, tag


def workload_to_helm_values(workload: dict[str, Any]) -> dict[str, Any]:
    spec = workload["spec"]
    repository, tag = split_image(spec["image"])

    ingress = spec.get("ingress", {})
    observability = spec.get("observability", {})

    values: dict[str, Any] = {
        "replicaCount": spec["replicas"],
        "image": {
            "repository": repository,
            "tag": tag,
        },
        "ingress": {
            "enabled": ingress.get("enabled", False),
        },
        "observability": {
            "enabled": observability.get("enabled", True),
        },
    }

    if "host" in ingress:
        values["ingress"]["host"] = ingress["host"]

    if "resources" in spec:
        values["resources"] = spec["resources"]

    return values


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Valida un Workload YAML e genera i valori per il chart Helm."
        )
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
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Percorso del file YAML di valori Helm da generare",
    )

    arguments = parser.parse_args()

    try:
        workload = load_yaml(arguments.workload)
        schema = load_schema(arguments.schema)
        errors = validate_workload(workload, schema)

        if errors:
            print(
                f"Workload non valido: {arguments.workload}",
                file=sys.stderr,
            )
            for error in errors:
                print(
                    f"- {format_location(error)}: {error.message}",
                    file=sys.stderr,
                )
            return 1

        if arguments.workload.resolve() == arguments.output.resolve():
            raise ValueError(
                "Il file di output non può sovrascrivere il Workload."
            )

        values = workload_to_helm_values(workload)

        with arguments.output.open("w", encoding="utf-8") as file:
            yaml.safe_dump(
                values,
                file,
                sort_keys=False,
                allow_unicode=True,
            )

    except (
        OSError,
        UnicodeDecodeError,
        yaml.YAMLError,
        json.JSONDecodeError,
        ValueError,
    ) as error:
        print(f"Errore: {error}", file=sys.stderr)
        return 1

    print(f"Valori Helm generati: {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())