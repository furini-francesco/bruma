# Avvio locale della demo Bruma

Questa guida descrive il flusso verificato per avviare la demo API in un
cluster Kubernetes locale Kind e controllare gli endpoint `/health` e
`/metrics`.

I comandi sono scritti per **Git Bash su Windows**, dalla cartella principale
del repository. La fase di produzione è lasciata come attività futura: non
eseguire i comandi locali come se fossero un deploy di produzione.

## Parte 1 - Requisiti

### Strumenti da installare

- **Git e Git Bash**, per scaricare il repository e lanciare i comandi.
- **Python 3.11 o successivo**, per validare i workload ed eseguire i test.
- **Docker Desktop**, configurato per usare Linux containers. Deve essere
  avviato durante la build dell'immagine e per tutto il tempo in cui il cluster
  Kind è attivo.
- **Kind**, per creare Kubernetes localmente usando Docker.
- **kubectl**, per interagire con il cluster Kubernetes.
- **Helm**, per installare il chart.
- **curl**, per verificare gli endpoint. È disponibile in Git Bash e nelle
  versioni recenti di Windows.

Per questa procedura non serve GNU Make: i comandi sono eseguiti direttamente
nel terminale. OpenTofu/Terraform e un account GitLab non sono necessari per il
test locale.

### Verifica degli strumenti

Aprire Git Bash e verificare che gli eseguibili siano disponibili:

```bash
python --version
docker version
kind version
kubectl version --client
helm version
curl --version
```

`docker version` deve mostrare sia la versione del client sia quella del server.
Se il server non è disponibile, avviare Docker Desktop prima di proseguire.

### Preparare l'ambiente Python

Dalla cartella principale del repository:

```bash
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r platform/validator/requirements.txt
```

Se `.venv` è già stata creata e le dipendenze installate, questo passaggio può
essere saltato.

## Parte 2 - Procedura Bruma

### Fase A - Test locale su Kind

#### 1. Verificare il codice e validare il workload

Eseguire i test automatizzati:

```bash
./.venv/Scripts/python.exe -m pytest platform/validator/tests apps/demo-api/tests -q
```

Validare il workload e generare i valori Helm:

```bash
./.venv/Scripts/python.exe platform/validator/workload_to_helm_values.py \
  platform/examples/demo-api-local.yaml \
  --output platform/examples/demo-api-local.values.yaml
```

Il file `demo-api-local.values.yaml` è generato dal comando e viene usato nei
passaggi Helm successivi.

#### 2. Controllare il chart Helm

```bash
helm lint platform/charts/app-runtime
helm template demo-api platform/charts/app-runtime \
  -f platform/examples/demo-api-local.values.yaml
```

`helm lint` controlla il chart; `helm template` stampa i manifest Kubernetes
renderizzati, ma non li applica al cluster.

#### 3. Costruire l'immagine Docker

Assicurarsi che Docker Desktop sia avviato e che il motore Linux sia pronto:

```bash
docker build -t bruma/demo-api:latest \
  -f apps/demo-api/Dockerfile \
  apps/demo-api
```

#### 4. Creare il cluster Kind

Questo comando va eseguito la prima volta, o dopo aver eliminato il cluster:

```bash
kind create cluster --name bruma
```

Kind configura anche il contesto `kind-bruma`. Per controllare il contesto e
lo stato del nodo:

```bash
kubectl config current-context
kubectl get nodes
```

Se il cluster `bruma` esiste già, non ricrearlo: controllarlo con
`kind get clusters` e continuare dal caricamento dell'immagine.

#### 5. Caricare l'immagine nel cluster

```bash
kind load docker-image bruma/demo-api:latest --name bruma
```

Il caricamento è necessario perché l'immagine è locale e non viene scaricata da
un registry.

#### 6. Installare la demo con Helm

```bash
helm upgrade --install demo-api platform/charts/app-runtime \
  -f platform/examples/demo-api-local.values.yaml \
  --namespace bruma \
  --create-namespace
```

Attendere che le repliche siano pronte e controllare i Pod:

```bash
kubectl rollout status deployment/demo-api-demo-api \
  --namespace bruma \
  --timeout=120s
kubectl get pods --namespace bruma
```

#### 7. Verificare `/health` e `/metrics`

In un primo terminale Git Bash, avviare il port-forward e lasciarlo attivo:

```bash
kubectl port-forward service/demo-api-demo-api 8080:80 \
  --namespace bruma
```

Aprire un secondo terminale Git Bash e verificare entrambi gli endpoint:

```bash
curl --fail --silent --show-error --include http://localhost:8080/health
curl --fail --silent --show-error --include http://localhost:8080/metrics
```

Le risposte attese sono `200 OK`. `/health` restituisce un JSON con lo stato
`healthy`; `/metrics` include la metrica `bruma_demo_api_up 1`.

#### 8. Terminare il test

Nel terminale del port-forward, premere `Ctrl+C`. Poi eliminare il cluster:

```bash
kind delete cluster --name bruma
```

Dopo la rimozione del cluster è possibile chiudere Docker Desktop. Eliminare
il cluster rimuove i Pod e le risorse Kubernetes del test, ma non il codice del
repository né l'immagine Docker locale.

### Fase B - Produzione (da definire)

La procedura di produzione non è ancora implementata. Prima di definirla
occorre decidere e documentare almeno:

- registry, tag immutabile e modalità di pubblicazione dell'immagine;
- ambiente Kubernetes di destinazione e credenziali;
- gestione di Ingress, controller, DNS e TLS;
- installazione/configurazione di Prometheus e raccolta delle metriche;
- secrets, permessi, configurazione e procedure di rollback;
- pipeline CI/CD e approvazioni per il rilascio.

Il test locale non pubblica l'immagine, non installa un controller Ingress e
non installa Prometheus. L'oggetto Ingress può essere renderizzato dal chart,
ma il suo host non sarà raggiungibile finché nel cluster non è configurato un
controller Ingress.
