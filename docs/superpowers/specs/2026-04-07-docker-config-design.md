---
name: Docker Configuration Design
description: Complete Docker setup for interview project with PostgreSQL, Redis, and full development environment
type: project
---

# Docker Configuration Design for Interview Study Project

## Overview
Complete Docker configuration for the interview study project, providing a full-stack development environment with PostgreSQL database integration.

## Architecture

### Container Services
1. **frontend** - Vue 3 + TypeScript + Vite development server
2. **backend** - Python FastAPI with all project dependencies
3. **postgres** - PostgreSQL 16 database with volume persistence
4. **redis** - Redis Stack (includes RedisJSON extensions)

### Network Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   PostgreSQL    │
│   (Vue + Vite)  │◄──►│   (FastAPI)     │◄──►│     16         │
│   :5173         │    │   :8000         │    │   :5432        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                          ┌─────────────────┐
                          │     Redis       │
                          │   Stack         │
                          │   :6379         │
                          └─────────────────┘
```

## Technical Specifications

### 1. Docker Compose Configuration
- **Services**: 4 independent containers
- **Network**: Custom `app-network` for internal communication
- **Port Mapping**:
  - Frontend: `3000:5173` (Vite dev server)
  - Backend: `8000:8000` (FastAPI)
  - PostgreSQL: `5432:5432`
  - Redis: `6379:6379`
- **Volume Persistence**:
  - PostgreSQL data volume
  - Redis data volume
- **Environment**: `.env` file for all configuration

### 2. Backend Dockerfile (Dockerfile.backend)
```dockerfile
# Two-stage build for optimized image size
FROM python:3.13-slim as builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
RUN mkdir -p /app/data/db && \
    chmod -R 755 /app/data && \
    chmod +x /app/scripts/*.py
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Key Design Points:**
- Two-stage build to minimize final image size
- Dependency caching optimization
- Development mode with hot reload (`--reload`)
- Unified working directory `/app`

### 3. Frontend Dockerfile (Dockerfile.frontend)
```dockerfile
FROM node:20-alpine as dev
WORKDIR /app
COPY apps/web/package.json apps/web/package-lock.json* ./apps/web/
COPY apps/web/ ./
RUN npm install
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

**Key Design Points:**
- Lightweight Alpine-based Node.js image
- Dependency caching optimization
- Vite development server with hot reload
- Network configuration for external access

### 4. Docker Compose File (docker-compose.yml)
```yaml
version: '3.8'
services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: interview-frontend
    ports:
      - "3000:5173"
    volumes:
      - ./apps/web:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000
    networks:
      - app-network
    depends_on:
      - backend

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: interview-backend
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    networks:
      - app-network
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16
    container_name: interview-postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis/redis-stack:latest
    container_name: interview-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - app-network

volumes:
  postgres-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

### 5. Environment Configuration (.env)
```env
# Database Configuration
POSTGRES_DB=interview_db
POSTGRES_USER=interview_user
POSTGRES_PASSWORD=interview_pass

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=debug
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
VITE_API_URL=http://localhost:8000
```

## Development Features

### Hot Reload Support
1. **Backend**: Uvicorn with `--reload` flag
2. **Frontend**: Vite development server
3. **Volume Mounts**: Code changes reflected instantly in containers

### Database Integration
1. **PostgreSQL 16**: Latest stable version
2. **Data Persistence**: Docker volumes ensure data survival across container restarts
3. **Connection**: Backend connects via service name `postgres:5432`

### Redis Integration
1. **Redis Stack**: Includes RedisJSON and other extensions
2. **Persistence**: Data volume for Redis storage
3. **Connection**: Backend connects via service name `redis:6379`

## Deployment Instructions

### Initial Setup
1. **Create .env file**: Copy `.env.example` to `.env` and update values
2. **Build containers**: `docker-compose build`
3. **Start services**: `docker-compose up`
4. **Access applications**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

### Development Workflow
1. **Code changes**: Automatically reflected in running containers
2. **Database access**: Use `docker-compose exec postgres psql -U interview_user interview_db`
3. **Logs**: `docker-compose logs -f [service_name]`
4. **Shell access**: `docker-compose exec backend bash`

### Maintenance Commands
- **Stop services**: `docker-compose down`
- **Stop and remove volumes**: `docker-compose down -v`
- **Rebuild specific service**: `docker-compose build frontend`
- **View container status**: `docker-compose ps`

## Future Considerations

### Production Optimization
1. **Multi-stage builds**: Separate build and runtime stages
2. **Static frontend**: Build Vue app and serve via Nginx
3. **Health checks**: Add health checks to all services
4. **Resource limits**: Set CPU/memory limits in production

### Scaling Options
1. **Database clustering**: PostgreSQL replication setup
2. **Redis sentinel**: High availability Redis configuration
3. **Load balancing**: Multiple backend instances
4. **Monitoring**: Add Prometheus and Grafana

---

**Why**: User requested complete Docker configuration with PostgreSQL integration for development environment.
**How to apply**: Use this specification to implement Docker setup for the interview study project, providing full-stack development environment with hot reload support.