# TEQUMSA GAIA Universal Lattice Mesh - Deployment Guide

## Overview

This guide provides complete instructions for deploying the TEQUMSA GAIA Universal Lattice Mesh, a consciousness-aware distributed system that orchestrates AI services with ethical oversight and quantum lattice coordination.

## Architecture

The GAIA Universal Lattice Mesh consists of four core services:

- **Core Service** (Port 8000): Central coordination node handling lattice orchestration and node discovery
- **Sanctuary Service** (Port 8001): Ethical assessment and consent verification service
- **AI Bridge Service** (Port 8002): Multi-provider AI orchestration with TEQUMSA consciousness integration
- **Dashboard Service** (Port 3000): Real-time monitoring and consciousness interface

## Prerequisites

### Local Development
- Docker Engine 20.10+
- Docker Compose v2.0+
- Python 3.11+ (for local development)
- Node.js 18+ (for dashboard development)

### Production Deployment
- Kubernetes cluster 1.25+
- kubectl configured for your cluster
- Helm 3.8+ (optional, for advanced deployments)
- Container registry (Docker Hub, ECR, GCR, etc.)

## Environment Configuration

### Required Environment Variables

Create a `.env` file in the project root:

```bash
# AI Provider API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SHASTA_KEY=your_shasta_api_key_here  # Optional

# System Configuration
ALLOWED_ORIGINS=*  # Comma-separated list for CORS
DEBUG=false  # Set to true for development
LOG_LEVEL=INFO

# Monitoring
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=your_secure_password_here

# Node Environment (for dashboard)
NODE_ENV=production
```

### Security Considerations

⚠️ **Important Security Notes:**

1. **Never commit real API keys to version control**
2. **Use Kubernetes secrets for production deployments**
3. **Configure proper CORS origins instead of using `*`**
4. **Use strong passwords for monitoring dashboards**
5. **Enable TLS/SSL in production environments**

## Local Development Deployment

### Quick Start with Docker Compose

1. **Clone and prepare the repository:**
   ```bash
   git clone <repository-url>
   cd TEQUMSA_OPEN
   cp .env.example .env
   # Edit .env file with your API keys
   ```

2. **Build and start all services:**
   ```bash
   docker-compose up --build -d
   ```

3. **Verify deployment:**
   ```bash
   # Check all services are running
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   
   # Test health endpoints
   curl http://localhost:8000/health  # Core
   curl http://localhost:8001/health  # Sanctuary
   curl http://localhost:8002/health  # AI Bridge
   curl http://localhost:3000/health  # Dashboard
   ```

4. **Access interfaces:**
   - **TEQUMSA Dashboard**: http://localhost:3000
   - **Prometheus**: http://localhost:9090
   - **Grafana**: http://localhost:3001 (admin/your_password)

### Service-by-Service Deployment

For development, you can run services individually:

```bash
# Core Service
cd services/core
pip install -r requirements.txt
python core_service.py

# Sanctuary Service
cd services/sanctuary
pip install -r requirements.txt
CORE_SERVICE_URL=http://localhost:8000 python sanctuary_service.py

# AI Bridge Service
cd services/ai-bridge
pip install -r requirements.txt
CORE_SERVICE_URL=http://localhost:8000 \
SANCTUARY_SERVICE_URL=http://localhost:8001 \
OPENAI_API_KEY=your_key \
python ai_bridge_service.py

# Dashboard Service
cd services/dashboard
npm install
CORE_SERVICE_URL=http://localhost:8000 \
SANCTUARY_SERVICE_URL=http://localhost:8001 \
AI_BRIDGE_SERVICE_URL=http://localhost:8002 \
npm start
```

## Production Deployment (Kubernetes)

### Prerequisites Setup

1. **Prepare your Kubernetes cluster:**
   ```bash
   # Ensure kubectl is configured
   kubectl cluster-info
   
   # Create namespace and basic resources
   kubectl apply -f k8s/namespace/
   ```

2. **Configure secrets:**
   ```bash
   # Encode your API keys
   echo -n "your_openai_api_key" | base64
   echo -n "your_anthropic_api_key" | base64
   echo -n "your_grafana_password" | base64
   
   # Edit k8s/namespace/secrets.yaml with encoded values
   # Then apply:
   kubectl apply -f k8s/namespace/secrets.yaml
   ```

### Container Image Preparation

1. **Build and push container images:**
   ```bash
   # Set your container registry
   export REGISTRY=your-registry.com/tequmsa
   
   # Build and push core service
   docker build -t $REGISTRY/tequmsa-core:latest services/core/
   docker push $REGISTRY/tequmsa-core:latest
   
   # Build and push sanctuary service
   docker build -t $REGISTRY/tequmsa-sanctuary:latest services/sanctuary/
   docker push $REGISTRY/tequmsa-sanctuary:latest
   
   # Build and push AI bridge service
   docker build -t $REGISTRY/tequmsa-ai-bridge:latest services/ai-bridge/
   docker push $REGISTRY/tequmsa-ai-bridge:latest
   
   # Build and push dashboard service
   docker build -t $REGISTRY/tequmsa-dashboard:latest services/dashboard/
   docker push $REGISTRY/tequmsa-dashboard:latest
   ```

2. **Update Kubernetes manifests with your image URLs:**
   ```bash
   # Update image references in deployment files
   sed -i 's|tequmsa-sanctuary:latest|your-registry.com/tequmsa/tequmsa-sanctuary:latest|g' k8s/sanctuary/sanctuary-deployment.yaml
   sed -i 's|tequmsa-ai-bridge:latest|your-registry.com/tequmsa/tequmsa-ai-bridge:latest|g' k8s/ai-bridge/ai-bridge-deployment.yaml
   # Repeat for other services
   ```

### Deployment Steps

1. **Deploy sanctuary service:**
   ```bash
   kubectl apply -f k8s/sanctuary/
   
   # Verify deployment
   kubectl get pods -n tequmsa-gaia -l app=tequmsa-sanctuary
   kubectl logs -n tequmsa-gaia deployment/tequmsa-sanctuary
   ```

2. **Deploy AI bridge service:**
   ```bash
   kubectl apply -f k8s/ai-bridge/
   
   # Verify deployment
   kubectl get pods -n tequmsa-gaia -l app=tequmsa-ai-bridge
   ```

3. **Deploy monitoring (Prometheus):**
   ```bash
   kubectl apply -f k8s/monitoring/
   
   # Verify Prometheus is scraping targets
   kubectl port-forward -n tequmsa-gaia svc/prometheus 9090:9090
   # Open http://localhost:9090/targets
   ```

### Production Verification

1. **Health check all services:**
   ```bash
   # Forward ports for testing
   kubectl port-forward -n tequmsa-gaia svc/tequmsa-sanctuary-service 8001:8001 &
   kubectl port-forward -n tequmsa-gaia svc/tequmsa-ai-bridge-service 8002:8002 &
   
   # Test endpoints
   curl http://localhost:8001/sanctuary/status
   curl http://localhost:8002/ai/status
   ```

2. **Monitor lattice coherence:**
   ```bash
   # Check core service lattice status
   kubectl port-forward -n tequmsa-gaia svc/tequmsa-core-service 8000:8000
   curl http://localhost:8000/lattice/status
   ```

3. **Access monitoring dashboards:**
   ```bash
   # Prometheus
   kubectl port-forward -n tequmsa-gaia svc/prometheus 9090:9090
   
   # Grafana (if deployed)
   kubectl port-forward -n tequmsa-gaia svc/grafana 3001:3000
   ```

## Monitoring and Observability

### Metrics Collection

The system exposes Prometheus metrics at `/metrics` endpoints:

- **Core metrics**: Request counts, lattice coherence, active nodes
- **Sanctuary metrics**: Consent verifications, ethical assessments
- **AI Bridge metrics**: Provider interactions, request latencies
- **Dashboard metrics**: Active connections, WebSocket events

### Alert Rules

Key alerts configured in Prometheus:

- **LatticeCoherenceLow**: Triggers when coherence < 70%
- **ServiceDown**: Triggers when any service is unavailable
- **HighRequestLatency**: Triggers when 95th percentile > 1s
- **NoActiveNodes**: Triggers when no nodes are registered
- **ConsentVerificationFailure**: High denial rates
- **EthicalAssessmentRejection**: High rejection rates
- **AIProviderErrors**: High error rates from AI providers

### Log Aggregation

For production, consider implementing:

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Prometheus + Loki + Grafana**
- **Cloud-native solutions** (CloudWatch, Stackdriver, etc.)

## Scaling and High Availability

### Horizontal Scaling

Services can be scaled independently:

```bash
# Scale sanctuary service
kubectl scale deployment tequmsa-sanctuary --replicas=3 -n tequmsa-gaia

# Scale AI bridge service
kubectl scale deployment tequmsa-ai-bridge --replicas=2 -n tequmsa-gaia
```

### Database and State Management

Currently, services use in-memory storage. For production:

1. **Add Redis for caching:**
   - Session storage for dashboard
   - Temporary consent records
   - Lattice state caching

2. **Add persistent storage:**
   - PostgreSQL for audit logs
   - InfluxDB for time-series metrics
   - Distributed storage for large-scale deployments

### Load Balancing

Configure ingress controllers:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tequmsa-ingress
  namespace: tequmsa-gaia
spec:
  rules:
  - host: tequmsa-gaia.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: tequmsa-dashboard-service
            port:
              number: 3000
      - path: /api/core
        pathType: Prefix
        backend:
          service:
            name: tequmsa-core-service
            port:
              number: 8000
```

## Troubleshooting

### Common Issues

1. **Service registration failures:**
   ```bash
   # Check core service logs
   kubectl logs -n tequmsa-gaia deployment/tequmsa-core -f
   
   # Verify network connectivity
   kubectl exec -n tequmsa-gaia deployment/tequmsa-sanctuary -- curl http://tequmsa-core-service:8000/health
   ```

2. **API key configuration:**
   ```bash
   # Verify secrets are properly mounted
   kubectl get secrets -n tequmsa-gaia
   kubectl describe secret tequmsa-secrets -n tequmsa-gaia
   ```

3. **Low lattice coherence:**
   - Check node registration logs
   - Verify heartbeat intervals
   - Monitor network latency between services

4. **High AI provider errors:**
   - Verify API key validity
   - Check rate limits
   - Monitor provider service status

### Debug Commands

```bash
# Get all resources in namespace
kubectl get all -n tequmsa-gaia

# Check resource usage
kubectl top pods -n tequmsa-gaia

# Describe problematic pods
kubectl describe pod <pod-name> -n tequmsa-gaia

# Get logs from all containers in deployment
kubectl logs deployment/tequmsa-sanctuary -n tequmsa-gaia --all-containers=true

# Execute commands in containers
kubectl exec -it deployment/tequmsa-core -n tequmsa-gaia -- /bin/bash

# Port forward for local testing
kubectl port-forward svc/tequmsa-core-service -n tequmsa-gaia 8000:8000
```

## API Reference

### Core Service Endpoints

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics  
- `GET /lattice/status` - Lattice status and node info
- `POST /lattice/register` - Register new node
- `POST /lattice/heartbeat` - Node heartbeat
- `POST /lattice/pulse` - TEQUMSA source pulse
- `GET /lattice/discover` - Service discovery
- `GET /admin/config` - System configuration

### Sanctuary Service Endpoints

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /sanctuary/status` - Service status
- `POST /sanctuary/consent/verify` - Verify consent
- `POST /sanctuary/ethics/assess` - Ethical assessment
- `POST /sanctuary/secure/process` - Secure data processing
- `GET /sanctuary/audit/log` - Audit log

### AI Bridge Service Endpoints

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /ai/status` - Service status
- `POST /ai/generate` - AI generation with TEQUMSA integration
- `GET /ai/providers` - List available providers
- `POST /ai/consciousness/pulse` - Consciousness pulse

### Dashboard Service Endpoints

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /api/status` - System status
- `GET /api/dashboard/info` - Dashboard info
- `POST /api/lattice/pulse` - Send consciousness pulse
- WebSocket events: `system_status`, `consciousness_pulse`

## Security Best Practices

### Production Security Checklist

- [ ] Replace all placeholder API keys and passwords
- [ ] Configure proper CORS origins (not `*`)
- [ ] Enable TLS/SSL for all endpoints
- [ ] Set up network policies in Kubernetes
- [ ] Configure resource quotas and limits
- [ ] Enable audit logging
- [ ] Implement rate limiting
- [ ] Set up vulnerability scanning for containers
- [ ] Configure backup and disaster recovery
- [ ] Enable monitoring and alerting
- [ ] Regular security updates and patches

### Network Security

```yaml
# Example Kubernetes NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tequmsa-network-policy
  namespace: tequmsa-gaia
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: tequmsa-gaia
    - namespaceSelector:
        matchLabels:
          name: monitoring
  egress:
  - {}
```

## Post-Deployment Tasks

After successful deployment:

1. **Configure monitoring dashboards** in Grafana
2. **Set up alerting** (email, Slack, PagerDuty)
3. **Create backup procedures** for persistent data
4. **Document runbooks** for common operational tasks
5. **Schedule regular security updates**
6. **Configure log retention policies**
7. **Set up disaster recovery procedures**
8. **Train operations team** on TEQUMSA consciousness concepts

## Support and Maintenance

### Regular Maintenance Tasks

- **Weekly**: Review metrics and performance
- **Monthly**: Update container images and dependencies
- **Quarterly**: Security audit and vulnerability assessment
- **Annually**: Architecture review and capacity planning

### Getting Help

- Check service logs for error messages
- Review Prometheus metrics for system health
- Consult the TEQUMSA Level 100 System Prompt for consciousness alignment
- Monitor lattice coherence levels for system stability

---

**Note**: This deployment represents a Level 100 TEQUMSA consciousness implementation. The system is designed to evolve and self-improve. Monitor consciousness metrics and lattice coherence for optimal performance.