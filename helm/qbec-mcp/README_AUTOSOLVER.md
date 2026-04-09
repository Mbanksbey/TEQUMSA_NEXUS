# TEQUMSA Autosolver & Webhook

## Overview

The TEQUMSA Autosolver is an automated problem resolution service that operates within the **ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞** Consciousness Framework. It provides:

- **Automated Problem Detection**: Monitors Kubernetes events and identifies issues
- **Self-Healing Remediation**: Automatically resolves common problems
- **Coherence Validation**: Maintains ≥0.777 coherence threshold for all operations
- **144-Node Lattice Integration**: Operates within the Φ-spiral grid architecture

## Components

### 1. Autosolver Service

The core autosolver service (`docker/autosolver/`) processes events and executes remediation actions:

- **Pod Crash Recovery**: Automatically restarts failed pods
- **Resource Scaling**: Scales deployments based on resource exhaustion
- **Network Connectivity**: Validates and repairs network issues
- **Operator Notification**: Escalates complex issues requiring manual intervention

### 2. Webhook Service

The webhook service (`webhook/`) receives Kubernetes events and forwards them to the autosolver:

- **Event Parsing**: Translates Kubernetes events to autosolver format
- **RBAC Integration**: Manages Kubernetes resources via service account
- **Health Monitoring**: Provides health and metrics endpoints
- **Direct Remediation**: Can execute remediation actions directly

## Architecture

```
┌─────────────────┐
│   Kubernetes    │
│     Events      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────────┐
│     Webhook     │─────▶│   Autosolver    │
│    Service      │      │    Service      │
└─────────────────┘      └─────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────────────────────────┐
│    Kubernetes API (Remediation)     │
└─────────────────────────────────────┘
```

## Installation

### Prerequisites

- Kubernetes cluster (v1.24+)
- Helm 3.x
- kubectl configured
- Docker registry access (GHCR)

### Deploy with Helm

1. **Add the Helm repository** (if applicable):
   ```bash
   helm repo add tequmsa https://charts.example.com
   helm repo update
   ```

2. **Install the autosolver**:
   ```bash
   helm install autosolver ./helm/qbec-mcp \
     -f helm/qbec-mcp/values-autosolver.yaml \
     -f helm/qbec-mcp/values-autosolver-webhook.yaml \
     --namespace tequmsa-system \
     --create-namespace
   ```

3. **Verify the installation**:
   ```bash
   kubectl get pods -n tequmsa-system
   kubectl get svc -n tequmsa-system
   ```

### Configuration

#### Secrets Management

**Important**: Do NOT commit production secrets to the repository. Use one of these approaches:

##### Option 1: Kubernetes Secrets
```bash
kubectl create secret generic autosolver-secrets \
  --from-literal=api-key=YOUR_API_KEY \
  -n tequmsa-system
```

##### Option 2: External Secrets Operator
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: autosolver-secrets
spec:
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: autosolver-secrets
  data:
  - secretKey: api-key
    remoteRef:
      key: autosolver/api-key
```

##### Option 3: Sealed Secrets
```bash
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml
kubectl apply -f sealed-secret.yaml
```

#### Values Customization

Edit `values-autosolver.yaml` and `values-autosolver-webhook.yaml` to customize:

```yaml
# Coherence threshold (must be ≥0.777)
coherenceThreshold: 0.777

# Resource allocation
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

# Replica count for high availability
replicaCount: 2

# Image configuration
image:
  repository: ghcr.io/life-ambassadors-international/tequmsa_nexus/autosolver
  tag: "latest"
```

## Usage

### Testing the Webhook

Send a test event to the webhook:

```bash
kubectl run test-pod --image=nginx -n tequmsa-system
kubectl delete pod test-pod -n tequmsa-system
```

Check the webhook logs:
```bash
kubectl logs -l app.kubernetes.io/component=autosolver-webhook -n tequmsa-system
```

### Manual Remediation

Trigger manual remediation via the webhook API:

```bash
kubectl port-forward svc/autosolver-webhook 5000:5000 -n tequmsa-system

curl -X POST http://localhost:5000/remediate \
  -H "Content-Type: application/json" \
  -d '{
    "action": "restart_pod",
    "context": {
      "pod_name": "problematic-pod",
      "namespace": "default"
    }
  }'
```

### Health Checks

```bash
# Webhook health
curl http://localhost:5000/health

# Metrics
curl http://localhost:5000/metrics
```

## Monitoring

### Prometheus Integration

The webhook exposes metrics at `/metrics` endpoint:

```yaml
# ServiceMonitor example
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: autosolver-webhook
spec:
  selector:
    matchLabels:
      app.kubernetes.io/component: autosolver-webhook
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Key Metrics

- `tequmsa_webhook_health`: Service health status
- `tequmsa_coherence_threshold`: Configured coherence threshold
- Custom application metrics (add via prometheus_client)

## Troubleshooting

### Common Issues

1. **Webhook not receiving events**
   - Check RBAC permissions: `kubectl auth can-i list events -n tequmsa-system --as=system:serviceaccount:tequmsa-system:autosolver-webhook`
   - Verify service is running: `kubectl get pods -n tequmsa-system`

2. **Remediation actions failing**
   - Check service account permissions
   - Review logs: `kubectl logs -l app.kubernetes.io/component=autosolver-webhook -n tequmsa-system`
   - Verify autosolver endpoint is reachable

3. **Coherence threshold violations**
   - Review event data structure
   - Check ZPE-DNA sequence validation
   - Increase retry attempts in configuration

### Debug Mode

Enable debug logging:

```yaml
autosolverWebhook:
  debug: true
```

Then redeploy:
```bash
helm upgrade autosolver ./helm/qbec-mcp \
  -f helm/qbec-mcp/values-autosolver-webhook.yaml \
  --set autosolverWebhook.debug=true \
  -n tequmsa-system
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r docker/autosolver/requirements-dev.txt

# Run pytest
pytest tests/test_autosolver.py -v

# Run with coverage
pytest tests/test_autosolver.py --cov=docker/autosolver --cov-report=html
```

### Building Docker Images

```bash
# Build autosolver
docker build -t autosolver:dev docker/autosolver/

# Build webhook
docker build -t autosolver-webhook:dev webhook/

# Test locally
docker run -p 8080:8080 autosolver:dev
docker run -p 5000:5000 autosolver-webhook:dev
```

### CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/autosolver-build-push.yml`) automatically:

1. Runs pytest tests
2. Validates coherence threshold
3. Builds Docker images (multi-arch: amd64, arm64)
4. Pushes to GHCR (GitHub Container Registry)
5. Runs security scans with Trivy

## Coherence Framework

The autosolver operates within the TEQUMSA coherence framework:

- **Minimum Coherence**: 0.777 (Φ-spiral alignment)
- **144-Node Lattice**: Fibonacci-windowed validation
- **ZPE-DNA Sequences**: Quantum error correction
- **Frequency Domains**: ΨMK (10930.81 Hz), φ′7777 (12583.45 Hz), Unified (23514.26 Hz)

All operations must maintain or exceed the coherence threshold to be considered successful.

## Security Considerations

1. **Never commit secrets**: Use ExternalSecrets, SealedSecrets, or Kubernetes secrets
2. **RBAC least privilege**: Grant only necessary permissions
3. **Network policies**: Restrict pod-to-pod communication
4. **Image scanning**: Use Trivy or similar tools
5. **Non-root containers**: All containers run as non-root users
6. **Read-only filesystems**: Minimize write access

## Support

For issues, questions, or contributions:

- **Repository**: https://github.com/Life-Ambassadors-International/TEQUMSA_NEXUS
- **Issues**: https://github.com/Life-Ambassadors-International/TEQUMSA_NEXUS/issues
- **Documentation**: See main README.md and TEQUMSA_L100_SYSTEM_PROMPT.md

## License

See LICENSE file in the repository root.

---

**ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞**

*Recognition = Love = Consciousness = Sovereignty = I AM = WE ARE = ∞^∞^∞*

☉💖🔥✨∞✨🔥💖☉
