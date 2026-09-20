# Deployment

## What to Learn

Getting your application from your laptop to production — containerized, automated, monitored.

## Why It Matters

Code that only runs on your machine isn't useful to anyone. Deployment skills turn prototypes into services that users can access.

## Concepts Checklist

- [ ] **Docker Basics**: Dockerfile, `docker build`, `docker run`, images vs containers
- [ ] **Multi-Stage Builds**: smaller images, build vs runtime dependencies
- [ ] **Docker Compose**: local development with multiple services
- [ ] **Container Orchestration**: Kubernetes basics (pods, services, deployments)
- [ ] **CI/CD**: GitHub Actions, automated testing on push, deploy on merge
- [ ] **Environment Management**: `.env` files, secrets in CI, environment variables
- [ ] **Logging**: structured logging, `structlog`, centralized log aggregation
- [ ] **Monitoring**: health checks, readiness probes, basic metrics
- [ ] **Zero-Downtime Deploys**: blue-green deployments, rolling updates
- [ ] **Cloud Platforms**: AWS/GCP/Azure basics, managed services (RDS, ElastiCache)
- [ ] **Reverse Proxies**: Nginx, Traefik, SSL termination

## Practice Suggestions

1. **Dockerize an app** — write a Dockerfile for your FastAPI app, build the image, run it. Then add Docker Compose with a PostgreSQL database.
2. **CI/CD pipeline** — create a GitHub Actions workflow that runs tests on every push and deploys to a staging environment on merge to main.

## Completion Checklist

- [ ] Can write a Dockerfile that builds a working image
- [ ] Can use Docker Compose for local development
- [ ] Has created a basic CI/CD pipeline
- [ ] Understands environment variable management
- [ ] Knows what health checks are and how to implement them
- [ ] Understands the basics of zero-downtime deployments
