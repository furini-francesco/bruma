#verifica YAML valido e YAML invalidi.
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[3]
VALIDATOR_DIR = ROOT_DIR / "platform" / "validator"

sys.path.insert(0, str(VALIDATOR_DIR))

from validate_workload import load_schema, load_yaml, validate_workload


SCHEMA_PATH = ROOT_DIR / "platform" / "schema" / "workload.schema.json"
VALID_WORKLOAD_PATH = (
    ROOT_DIR / "platform" / "examples" / "demo-api-local.yaml"
)


def test_demo_workload_is_valid():
    workload = load_yaml(VALID_WORKLOAD_PATH)
    schema = load_schema(SCHEMA_PATH)

    errors = validate_workload(workload, schema)

    assert errors == []


def test_replicas_cannot_be_zero():
    workload = load_yaml(VALID_WORKLOAD_PATH)
    workload["spec"]["replicas"] = 0
    schema = load_schema(SCHEMA_PATH)

    errors = validate_workload(workload, schema)

    assert len(errors) == 1
    assert list(errors[0].absolute_path) == ["spec", "replicas"]


def test_unknown_environment_is_rejected():
    workload = load_yaml(VALID_WORKLOAD_PATH)
    workload["metadata"]["environment"] = "staging"
    schema = load_schema(SCHEMA_PATH)

    errors = validate_workload(workload, schema)

    assert len(errors) == 1
    assert list(errors[0].absolute_path) == ["metadata", "environment"]


def test_unknown_property_is_rejected():
    workload = load_yaml(VALID_WORKLOAD_PATH)
    workload["spec"]["kubernetesDeployment"] = {}
    schema = load_schema(SCHEMA_PATH)

    errors = validate_workload(workload, schema)

    assert len(errors) == 1
    assert list(errors[0].absolute_path) == ["spec"]
    assert "kubernetesDeployment" in errors[0].message