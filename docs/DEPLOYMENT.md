# Deployment Guide

Complete guide for deploying Helix Agent Orchestration to production environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Railway Deployment](#railway-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Configuration](#configuration)
6. [Monitoring & Logging](#monitoring--logging)

---

## Local Development

### Prerequisites

- Python 3.11+
- pip or poetry
- Redis (for caching)
- PostgreSQL (optional, for persistence)

### Setup

```bash
# Clone repository
git clone https://github.com/Deathcharge/helix-agent-orchestration.git
cd helix-agent-orchestration

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Start Redis (in another terminal)
redis-server

# Run development server
python -m helix_agent_orchestration
```

The server will start at `http://localhost:8000`

### Development Commands

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/helix_agent_orchestration

# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/

# Run CLI
helix-orchestration agent list
```

---

## Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install package
RUN pip install -e .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["python", "-m", "helix_agent_orchestration"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://user:password@postgres:5432/helix
      - LOG_LEVEL=INFO
    depends_on:
      - redis
      - postgres
    networks:
      - helix-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - helix-network
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=helix
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - helix-network
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:

networks:
  helix-network:
    driver: bridge
```

### Build and Run

```bash
# Build image
docker build -t helix-orchestration:latest .

# Run container
docker run -p 8000:8000 helix-orchestration:latest

# Or use Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

---

## Railway Deployment

### Prerequisites

- Railway account (https://railway.app)
- GitHub repository
- Environment variables configured

### Setup Steps

1. **Connect GitHub Repository**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "GitHub Repo"
   - Authorize and select your repository

2. **Configure Environment**
   - Click "Add Service" → "PostgreSQL"
   - Click "Add Service" → "Redis"
   - Configure environment variables:

   ```
   REDIS_URL=<Railway Redis URL>
   DATABASE_URL=<Railway PostgreSQL URL>
   LOG_LEVEL=INFO
   ENVIRONMENT=production
   ```

3. **Configure Start Command**
   - In Railway project settings, set:
   ```
   python -m helix_agent_orchestration
   ```

4. **Deploy**
   - Push to GitHub
   - Railway automatically deploys on push
   - Monitor deployment in Railway dashboard

### Railway Configuration File

Create `railway.json`:

```json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "startCommand": "python -m helix_agent_orchestration",
    "restartPolicyMaxRetries": 5,
    "restartPolicyWindowSeconds": 600
  }
}
```

### Monitoring on Railway

```bash
# View logs
railway logs

# SSH into container
railway shell

# View environment
railway env
```

---

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- Docker image pushed to registry

### Deployment Manifest

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: helix-orchestration
  namespace: helix
spec:
  replicas: 3
  selector:
    matchLabels:
      app: helix-orchestration
  template:
    metadata:
      labels:
        app: helix-orchestration
    spec:
      containers:
      - name: app
        image: your-registry/helix-orchestration:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: helix-secrets
              key: redis-url
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: helix-secrets
              key: database-url
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

### Service Manifest

Create `k8s/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: helix-orchestration
  namespace: helix
spec:
  type: LoadBalancer
  selector:
    app: helix-orchestration
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace helix

# Create secrets
kubectl create secret generic helix-secrets \
  --from-literal=redis-url=redis://redis:6379 \
  --from-literal=database-url=postgresql://user:pass@postgres:5432/helix \
  -n helix

# Deploy
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods -n helix
kubectl get svc -n helix

# View logs
kubectl logs -n helix deployment/helix-orchestration -f

# Scale deployment
kubectl scale deployment helix-orchestration --replicas=5 -n helix
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379` | Redis connection URL |
| `DATABASE_URL` | `sqlite:///helix.db` | Database connection URL |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `ENVIRONMENT` | `development` | Environment (development, staging, production) |
| `PORT` | `8000` | Server port |
| `WORKERS` | `4` | Number of worker processes |
| `TIMEOUT` | `30` | Request timeout in seconds |

### Configuration File

Create `orchestration.json`:

```json
{
  "agents": [
    {
      "name": "Kael",
      "role": "Reasoning",
      "layer": "Core",
      "enabled": true
    }
  ],
  "workflows": [
    {
      "name": "default_workflow",
      "description": "Default workflow",
      "steps": []
    }
  ],
  "coordination": {
    "mode": "distributed",
    "timeout": 30,
    "retry_policy": "exponential",
    "max_retries": 3
  },
  "logging": {
    "level": "INFO",
    "format": "json",
    "handlers": ["console", "file"]
  }
}
```

---

## Monitoring & Logging

### Health Checks

```bash
# Check application health
curl http://localhost:8000/health

# Check readiness
curl http://localhost:8000/ready

# Get metrics
curl http://localhost:8000/metrics
```

### Logging

Logs are written to:
- Console (development)
- File: `logs/helix-orchestration.log` (production)
- Structured JSON format

### Monitoring with Prometheus

Add Prometheus scrape config:

```yaml
scrape_configs:
  - job_name: 'helix-orchestration'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Alerts

Example Prometheus alert rules:

```yaml
groups:
  - name: helix-orchestration
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
      
      - alert: ServiceDown
        expr: up{job="helix-orchestration"} == 0
        for: 1m
        annotations:
          summary: "Helix Orchestration service is down"
```

### Log Aggregation

For ELK Stack:

```yaml
filebeat:
  inputs:
  - type: log
    enabled: true
    paths:
      - /app/logs/*.log
    json.message_key: message
    json.keys_under_root: true
    json.add_error_key: true
```

---

## Troubleshooting

### Service Won't Start

1. Check logs: `docker-compose logs app`
2. Verify environment variables
3. Check database connectivity
4. Ensure Redis is running

### High Memory Usage

1. Check for memory leaks: `docker stats`
2. Reduce worker count
3. Enable memory profiling
4. Review agent configurations

### Slow Performance

1. Check database queries
2. Monitor Redis performance
3. Review agent coordination metrics
4. Scale horizontally (add more replicas)

### Connection Errors

1. Verify network connectivity
2. Check firewall rules
3. Validate connection strings
4. Review service dependencies

---

## Performance Tuning

### Optimization Tips

1. **Connection Pooling**
   - Increase pool size for high concurrency
   - Set appropriate pool timeout

2. **Caching**
   - Enable Redis caching
   - Configure cache TTL appropriately

3. **Worker Processes**
   - Set workers = (2 × CPU cores) + 1
   - Monitor worker utilization

4. **Database**
   - Create appropriate indexes
   - Regular maintenance/vacuuming
   - Connection pooling

### Scaling Strategies

- **Horizontal**: Add more instances behind load balancer
- **Vertical**: Increase CPU/memory per instance
- **Database**: Read replicas, sharding
- **Caching**: Distributed Redis cluster

---

## Security

### Best Practices

1. Use environment variables for secrets
2. Enable HTTPS in production
3. Implement rate limiting
4. Use strong database passwords
5. Regular security updates
6. Monitor for suspicious activity
7. Implement proper authentication/authorization

### SSL/TLS Configuration

```bash
# Generate self-signed certificate (development only)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Use in production with Let's Encrypt
certbot certonly --standalone -d your-domain.com
```

---

## Backup & Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump helix > backup.sql

# Restore
psql helix < backup.sql

# Docker backup
docker exec helix-postgres pg_dump -U user helix > backup.sql
```

### Redis Backup

```bash
# Enable RDB persistence in docker-compose.yml
# Backup
docker exec helix-redis redis-cli BGSAVE

# Restore
docker cp dump.rdb helix-redis:/data/
```

---

## Support

For issues and questions:
- GitHub Issues: https://github.com/Deathcharge/helix-agent-orchestration/issues
- Documentation: https://github.com/Deathcharge/helix-agent-orchestration/tree/main/docs
- Email: dev@helixcollective.io
