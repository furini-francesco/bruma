 <p align="center">
  <img src="assets/bruma-cover.png" alt="Bruma — Navigating cloud-native infrastructure through the fog" width="100%">
</p>

<h1 align="center">Bruma</h1>

<p align="center">
  <em>Navigate the complexity of cloud-native infrastructure.</em>
</p>

<p align="center">
  A local-first Kubernetes delivery platform.
</p>

# Bruma

> Da una definizione dichiarativa a un deployment Kubernetes sicuro, osservabile e riproducibile.

[![CI](https://img.shields.io/badge/CI-GitLab-blue)](https://gitlab.com/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Kind-blue)](https://kind.sigs.k8s.io/)
[![Terraform](https://img.shields.io/badge/IaC-OpenTofu-purple)](https://opentofu.org/)

**Bruma** è una piattaforma di riferimento *local-first* per il delivery di applicazioni su Kubernetes.

Partendo da un file YAML dichiarativo, Bruma valida la configurazione, renderizza un Helm chart, esegue test e deploy su un cluster Kubernetes locale con Kind e integra sicurezza, osservabilità e rollback.

Il progetto è pensato per essere eseguito e testato **a costo zero**, usando Docker e Kind. Le integrazioni con AWS, GCP e Azure sono moduli opzionali e richiedono credenziali cloud.

## Perché Bruma

Bruma mostra un flusso end-to-end di platform engineering:

- Definizione dichiarativa del workload tramite YAML.
- Validazione della configurazione prima del deploy.
- Build, test e scansione dell’immagine container.
- Deployment Helm su Kubernetes.
- Osservabilità con metriche e dashboard.
- Rollback controllato in caso di deploy non valido.
- Infrastruttura cloud opzionale tramite Terraform/OpenTofu.

Non è un prodotto enterprise completo: è un progetto tecnico modulare, documentato e riproducibile, utile come riferimento per team che vogliono adottare pratiche di delivery Kubernetes.

## Funzionalità

- **Workload self-service:** descrivi l’applicazione in un file YAML.
- **Validazione:** schema JSON per verificare la configurazione prima del deploy.
- **Helm runtime:** chart riutilizzabile per Deployment, Service, Ingress, ConfigMap e ServiceAccount.
- **Kubernetes locale:** test su Kind con Docker.
- **GitLab CI/CD:** lint, test, build, sicurezza, deploy e rollback.
- **Sicurezza:** scansione delle immagini con Trivy e analisi IaC con Checkov.
- **Osservabilità:** metriche Prometheus e dashboard Grafana.
- **Multi-cloud opzionale:** moduli Terraform/OpenTofu per AWS, GCP e Azure.

## Architettura

```text
workload.yaml
     │
     ▼
Validazione schema
     │
     ▼
GitLab CI/CD
     │
     ├── Lint e unit test
     ├── Build immagine Docker
     ├── Scansione Trivy
     ├── Helm render
     └── Deploy su Kind
     │
     ▼
Kubernetes / Kind
     │
     ├── App demo
     ├── Prometheus
     └── Grafana
```

## Requisiti

Per la demo locale servono:

- Docker
- Kubernetes CLI (`kubectl`)
- Kind
- Helm
- Python 3.11+
- OpenTofu oppure Terraform
- GitLab account per la pipeline CI/CD

## Avvio rapido

Clona il repository:

```bash
git clone [https://github.com/](https://github.com/)<tuo-username>/bruma.git
cd bruma
```

Installa le dipendenze e avvia l’ambiente locale:

```bash
make setup
make kind-up
```

Esegui la demo:

```bash
make deploy-local
make smoke-test
```

Apri l’applicazione:

```bash
kubectl port-forward svc/demo-api 8080:80 -n bruma
```

Poi visita:

```text
http://localhost:8080/health
```

## Esempio di workload

```yaml
apiVersion: bruma.io/v1alpha1
kind: Workload
metadata:
  name: demo-api
  environment: local
spec:
  image: ghcr.io/<tuo-username>/bruma-demo-api:latest
  replicas: 2
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi
  ingress:
    enabled: true
    host: demo.local
  observability:
    enabled: true
```

## Comandi utili

| Comando | Descrizione |
|---|---|
| `make setup` | Installa e verifica gli strumenti locali |
| `make lint` | Esegue lint e validazioni |
| `make test` | Esegue i test dell’applicazione |
| `make docker-build` | Build dell’immagine demo |
| `make kind-up` | Crea il cluster Kubernetes locale |
| `make kind-down` | Elimina il cluster locale |
| `make deploy-local` | Deploy dell’app demo su Kind |
| `make smoke-test` | Verifica health e disponibilità |
| `make observability-up` | Installa Prometheus e Grafana |
| `make clean` | Rimuove risorse locali temporanee |

## Struttura del progetto

```text
bruma/
├── apps/          # Applicazione demo
├── platform/      # Schema, Helm chart e script della piattaforma
├── infra/         # Moduli Terraform/OpenTofu e ambienti
├── tests/         # Test di integrazione, sicurezza e load
├── ci/            # Template GitLab CI/CD
└── docs/          # Architettura, runbook e decisioni tecniche
```

## Stato del progetto

| Area | Stato |
|---|---|
| App demo | In sviluppo |
| Helm chart base | In sviluppo |
| Deploy su Kind | In sviluppo |
| GitLab CI/CD | In sviluppo |
| Sicurezza | Pianificata |
| Osservabilità | Pianificata |
| AWS | Opzionale, non ancora implementato |
| GCP | Opzionale, non ancora implementato |
| Azure | Opzionale, non ancora implementato |

Feature da implementare:
- partenza: definizione contratto YAML
  - Decidere dove salvare lo schema.
  - Creare un esempio minimo e valido.
  - Definire i campi obbligatori.
  - Imporre vincoli su replica, risorse e ambiente.
  - Documentare il contratto.
  - Verificare lo YAML con JSON Schema.
- API demo con endpoint /health
- dockerfile funzionante
- test automatizzato dell'health check
- deployment con Helm su un cluster Kind
- comando make smoke-test che verifica l'applicazione risponda
- singola demo locale completa 

## Limiti noti

- La demo pubblica usa Kind e non richiede account cloud.
- Le integrazioni AWS, GCP e Azure richiedono credenziali e account cloud propri.
- La pipeline GitLab usa la quota gratuita: i test pesanti sono progettati per essere eseguibili anche in locale.
- Bruma non sostituisce una piattaforma Internal Developer Platform completa.

## Documentazione

- [Architettura](docs/architecture.md)
- [Avvio rapido](docs/getting-started.md)
- [Sviluppo locale](docs/local-development.md)
- [CI/CD](docs/ci-cd.md)
- [Sicurezza](docs/security.md)
- [Osservabilità](docs/observability.md)
- [Cloud provider](docs/cloud-providers.md)

## Contribuire

Le contribuzioni sono benvenute. Apri una issue per proporre una modifica oppure invia una pull request con test e documentazione aggiornata.

## Licenza

Distribuito sotto licenza [Apache License 2.0](LICENSE).