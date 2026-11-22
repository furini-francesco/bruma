# Architettura

Questo documento descrive l'architettura prevista di Bruma e il flusso dal file dichiarativo al deployment Kubernetes.

## Obiettivi

- Definire i workload in modo dichiarativo.
- Validare la configurazione prima del deployment.
- Distribuire applicazioni in modo sicuro e riproducibile.
- Nascondere i dettagli Kubernetes agli sviluppatori.
- Offrire un ambiente locale con Kind.
- Supportare osservabilità, rollback e integrazioni cloud opzionali.

## Contratto pubblico: Workload YAML

Bruma espone agli utenti un formato dichiarativo chiamato `Workload`.

Un esempio è:

```yaml
apiVersion: bruma.io/v1
kind: Workload
metadata:
  name: demo-api
  environment: local
spec:
  image: bruma/demo-api:latest
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

### Campi principali
- *apiVersion*: identifica la versione del formato Bruma.
- *kind*: identifica il tipo di risorsa; per ora il tipo supportato è Workload.
- *metadata.name*: nome dell'applicazione.
- *metadata.environment*: ambiente di destinazione, come local, development o production.
- *spec.image*: immagine container da distribuire.
- *spec.replicas*: numero di istanze richieste.
- *spec.resources*: risorse CPU e memoria richieste o consentite.
- *spec.ingress*: configurazione opzionale dell'esposizione HTTP.
- *spec.observability*: configurazione opzionale della raccolta di metriche.