# Deployment Guide

## Local Development

See [Getting Started](getting-started.md)

## Docker Deployment

### Build Image

```bash
docker build -t ai-agent-builder:latest .
```

### Run Container

```bash
docker run -p 8000:8000 \\
  -e DATABASE_URL=postgresql://... \\
  -e LLM_PROVIDER=ollama \\
  ai-agent-builder:latest
```

## Production Considerations

### Database

Use managed PostgreSQL:
- AWS RDS
- Google Cloud SQL
- Azure Database

Update DATABASE_URL in .env

### LLM Provider

For production, consider:
- **Ollama** - Self-hosted on server
- **Groq** - Cloud API (fast, free tier)

### Performance

- Enable connection pooling (default)
- Use smaller LLM models for speed
- Monitor with logging
- Set appropriate pool size (DB_POOL_MAX)

### Security

**Before public deployment:**
1. Add authentication
2. Add rate limiting
3. Enable HTTPS
4. Set CORS_ORIGINS to your domain
5. Use strong database credentials

### Monitoring

Add monitoring:
- Log aggregation (ELK, CloudWatch)
- Error tracking (Sentry)
- Performance metrics (Prometheus)

## Cloud Deployment

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render

```bash
# Connect GitHub repo
# Add environment variables
# Deploy automatically on push
```

### AWS

See detailed AWS guide in docs/aws-deployment.md

## Environment Variables

Production .env:

```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...
CORS_ORIGINS=https://yourdomain.com
```