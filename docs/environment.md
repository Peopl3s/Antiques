# Environment Configuration

## Overview

The application uses environment variables for configuration. All variables are defined in the `.env` file and can be customized for different environments.

## Setup

### 1. Create .env file

```bash
# Copy from template
make setup-env

# Or manually copy
cp env.template .env
```

### 2. Customize variables

Edit the `.env` file to match your environment:

```bash
# Application Configuration
ENVIRONMENT=dev
LOG_LEVEL=DEBUG
DEBUG=true

# Database Configuration
POSTGRES_USER=antiques_user
POSTGRES_PASSWORD=antiques_password
POSTGRES_SERVER=postgres
POSTGRES_PORT=5432
POSTGRES_DB=antiques

# External APIs
MUSEUM_API_BASE=https://api.antiquarium-museum.ru
CATALOG_API_BASE=https://catalog.antiquarium-museum.ru
HTTP_TIMEOUT=10.0

# Message Broker (Kafka)
BROKER_URL=kafka://kafka:9092
BROKER_NEW_ARTIFACT_QUEUE=new_artifacts

# Retry Configuration
PUBLISH_RETRIES=3
PUBLISH_RETRY_BACKOFF=0.5
```

## Environment Variables

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `dev` | Application environment (dev, prod, testing) |
| `LOG_LEVEL` | `DEBUG` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `DEBUG` | `true` | Enable debug mode |

### Database Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `antiques_user` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `antiques_password` | PostgreSQL password |
| `POSTGRES_SERVER` | `postgres` | PostgreSQL hostname |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `POSTGRES_DB` | `antiques` | PostgreSQL database name |

### External APIs

| Variable | Default | Description |
|----------|---------|-------------|
| `MUSEUM_API_BASE` | `https://api.antiquarium-museum.ru` | Museum API base URL |
| `CATALOG_API_BASE` | `https://catalog.antiquarium-museum.ru` | Catalog API base URL |
| `HTTP_TIMEOUT` | `10.0` | HTTP request timeout in seconds |

### Message Broker (Kafka)

| Variable | Default | Description |
|----------|---------|-------------|
| `BROKER_URL` | `kafka://kafka:9092` | Kafka broker URL |
| `BROKER_NEW_ARTIFACT_QUEUE` | `new_artifacts` | Kafka topic for new artifacts |

### Retry Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PUBLISH_RETRIES` | `3` | Number of retry attempts |
| `PUBLISH_RETRY_BACKOFF` | `0.5` | Backoff delay between retries |

## Docker Compose Integration

Docker Compose automatically loads variables from the `.env` file using the `${VARIABLE:-default}` syntax:

```yaml
environment:
  ENVIRONMENT: ${ENVIRONMENT:-dev}
  LOG_LEVEL: ${LOG_LEVEL:-DEBUG}
  POSTGRES_USER: ${POSTGRES_USER}
  # ... other variables
```

## Environment-specific Configurations

### Development

```bash
ENVIRONMENT=dev
LOG_LEVEL=DEBUG
DEBUG=true
```

### Production

```bash
ENVIRONMENT=prod
LOG_LEVEL=INFO
DEBUG=false
```

### Testing

```bash
ENVIRONMENT=testing
LOG_LEVEL=INFO
DEBUG=false
```

## Security Notes

- Never commit `.env` files to version control
- Use strong passwords in production
- Consider using Docker secrets for sensitive data
- Rotate credentials regularly

## Troubleshooting

### Missing Variables

If a required variable is missing, Docker Compose will show an error:

```
WARNING: The POSTGRES_USER variable is not set. Defaulting to a blank string.
```

### Invalid Values

Check the application logs for validation errors:

```bash
docker-compose logs app-dev
```

### Environment File Not Found

Make sure the `.env` file exists in the project root:

```bash
ls -la .env
```
