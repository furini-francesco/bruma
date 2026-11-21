# Architecture

This document describes the planned architecture of Bruma.

## Goals

- Declarative environment definition
- Safe and reproducible deployments
- Observability and operational clarity
- Modular infrastructure structure

## Structure

- `apps/` contains application code
- `platform/` contains runtime and deployment assets
- `infra/` contains infrastructure modules and environment definitions
- `docs/` contains project documentation

## Workload YAML

- JSON Schema
- validatore Python
- valori per Helm
- chart app-runtime
- Kubernetes/Kind