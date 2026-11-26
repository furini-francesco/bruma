CLUSTER_NAME ?= bruma
NAMESPACE ?= bruma
RELEASE ?= demo-api
IMAGE ?= bruma/demo-api:latest
CHART_DIR := platform/charts/app-runtime
VALUES_FILE := platform/examples/demo-api-local.values.yaml

.PHONY: help image-build kind-up kind-load deploy-local port-forward smoke-test kind-down

help:
    @echo "Bruma local development"
    @echo "  make image-build   Build the demo API Docker image"
    @echo "  make kind-up       Create the local Kind cluster if needed"
    @echo "  make deploy-local  Build, load and deploy the app to Kind"
    @echo "  make port-forward  Forward the app to localhost:8080"
    @echo "  make smoke-test    Check /health and /metrics"
    @echo "  make kind-down     Delete the local Kind cluster"

image-build:
    docker build -t $(IMAGE) -f apps/demo-api/Dockerfile apps/demo-api

kind-up:
    @kind get clusters | grep -qx "$(CLUSTER_NAME)" || kind create cluster --name "$(CLUSTER_NAME)"

kind-load: image-build kind-up
    kind load docker-image $(IMAGE) --name $(CLUSTER_NAME)

deploy-local: kind-load
    helm upgrade --install $(RELEASE) $(CHART_DIR) \
        -f $(VALUES_FILE) \
        --namespace $(NAMESPACE) \
        --create-namespace
    kubectl rollout status deployment/$(RELEASE)-demo-api \
        --namespace $(NAMESPACE) \
        --timeout=120s

port-forward:
    kubectl port-forward service/$(RELEASE)-demo-api 8080:80 \
        --namespace $(NAMESPACE)

smoke-test:
    curl --fail --silent --show-error http://localhost:8080/health
    curl --fail --silent --show-error http://localhost:8080/metrics

kind-down:
    kind delete cluster --name $(CLUSTER_NAME)