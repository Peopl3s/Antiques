# Docker Setup для Antiques

Этот документ описывает настройку и использование Docker для приложения Antiques.

## Структура Docker

### Multi-stage Dockerfile

Dockerfile использует multi-stage сборку для оптимизации размера образа:

1. **base** - базовый образ с системными зависимостями
2. **deps** - установка production зависимостей
3. **deps-dev** - установка development зависимостей
4. **production** - production образ
5. **development** - development образ с hot reload
6. **testing** - образ для запуска тестов

### Best Practices

- ✅ Использование non-root пользователя
- ✅ Multi-stage сборка для уменьшения размера
- ✅ Кеширование зависимостей с uv
- ✅ Health checks для всех сервисов
- ✅ Proper signal handling
- ✅ Минимальный базовый образ (python:3.12-slim-bookworm)

## Команды Docker

### Сборка образов

```bash
# Production образ
make docker-build

# Development образ
make docker-build-dev

# Testing образ
make docker-build-test
```

### Запуск сервисов

```bash
# Запуск всех сервисов (production)
make docker-up

# Запуск development окружения
make docker-up-dev

# Остановка всех сервисов
make docker-down
```

### Работа с базой данных

```bash
# Запуск миграций
make docker-migrate

# Подключение к базе данных
docker-compose exec postgres psql -U antiques_user -d antiques
```

### Тестирование

```bash
# Запуск тестов в Docker
make docker-test

# Просмотр отчетов о покрытии
docker-compose --profile test run --rm test
```

### Отладка

```bash
# Просмотр логов
make docker-logs

# Логи только приложения
make docker-logs-app

# Подключение к контейнеру
make docker-shell
```

## Docker Compose Profiles

### production (по умолчанию)
- app (production)
- postgres
- redis

### dev
- app-dev (с hot reload)
- postgres (с exposed портами)
- redis (с exposed портами)

### migrate
- migrate (запуск миграций)

### test
- test (запуск тестов)

### nginx
- nginx (reverse proxy)

### dev-tools
- adminer (веб-интерфейс для БД)

## Переменные окружения

### Обязательные
- `DATABASE_URL` - URL подключения к PostgreSQL
- `REDIS_URL` - URL подключения к Redis

### Опциональные
- `ENVIRONMENT` - окружение (production/development/testing)
- `LOG_LEVEL` - уровень логирования
- `API_HOST` - хост для API
- `API_PORT` - порт для API
- `API_WORKERS` - количество worker процессов

## Volumes

### Named Volumes
- `postgres_data` - данные PostgreSQL
- `redis_data` - данные Redis
- `app_logs` - логи приложения
- `test_reports` - отчеты тестов

### Bind Mounts (development)
- `./src:/app/src` - исходный код
- `./tests:/app/tests` - тесты
- `./alembic:/app/alembic` - миграции

## Сетевые настройки

Все сервисы подключены к сети `antiques-network` для изоляции.

## Health Checks

Все сервисы имеют health checks:
- **app**: HTTP запрос к `/api/docs`
- **postgres**: `pg_isready`
- **redis**: `redis-cli ping`

## Безопасность

- Использование non-root пользователя в контейнерах
- Изоляция сервисов в отдельной сети
- Переменные окружения для секретов
- Минимальные базовые образы

## Мониторинг

### Логи
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f app
```

### Метрики
- Health checks для всех сервисов
- Логирование в JSON формате
- Возможность интеграции с Sentry

## Troubleshooting

### Проблемы с подключением к БД
```bash
# Проверить статус PostgreSQL
docker-compose exec postgres pg_isready -U antiques_user

# Проверить логи
docker-compose logs postgres
```

### Проблемы с Redis
```bash
# Проверить подключение к Redis
docker-compose exec redis redis-cli ping

# Проверить логи
docker-compose logs redis
```

### Пересборка образов
```bash
# Полная пересборка
make docker-rebuild

# Очистка ресурсов
make docker-clean
```

## Production Deployment

### Рекомендации для production

1. **Используйте production образ**:
   ```bash
   docker build --target production -t antiques:latest .
   ```

2. **Настройте переменные окружения**:
   ```bash
   export DATABASE_URL="postgresql+asyncpg://user:pass@db:5432/antiques"
   export REDIS_URL="redis://:pass@redis:6379/0"
   export ENVIRONMENT="production"
   ```

3. **Используйте внешние volumes**:
   ```yaml
   volumes:
     - /var/lib/antiques/postgres:/var/lib/postgresql/data
     - /var/lib/antiques/redis:/data
     - /var/log/antiques:/app/logs
   ```

4. **Настройте reverse proxy** (nginx):
   ```bash
   docker-compose --profile nginx up -d
   ```

5. **Мониторинг**:
   - Настройте логирование
   - Используйте health checks
   - Мониторьте ресурсы

### Docker Swarm / Kubernetes

Для production можно использовать:
- Docker Swarm для простого оркестрирования
- Kubernetes для более сложных сценариев
- Docker Compose для single-host deployment
