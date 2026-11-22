# Getting Started
Il primo passo consiste nello scrivere un file Workload YAML.
Bruma lo validerà rispetto a platform/schema/workload.schema.json.
Solo un workload valido potrà essere convertito in risorse Kubernetes.

## Prerequisites

- Git
- Docker
- Kubernetes tooling (optional for local validation)
- Make

## Quick start

1. Clone the repository.
2. Review the repo structure.
3. Start from the `apps/demo-api` service.
4. Use the Makefile for common project commands.

## Next steps

- Define the application contract
- Add deployment manifests
- Configure environment variables
- Add CI validation rules
