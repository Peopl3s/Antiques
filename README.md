# Antiques API

API для управления артефактами в музее антиквариата.

## Описание

Antiques - это современное веб-приложение для управления коллекцией артефактов в музее. Приложение построено на FastAPI с использованием чистой архитектуры (Clean Architecture) и современных практик разработки.

## Основные возможности

- 🔍 Поиск артефактов
- 🐳 Docker контейнеризация
- 🗄️ PostgreSQL база данных
- ⚡ Redis кеширование
- 📝 Автоматическая документация API

## Технологический стек

- **Backend**: Python 3.12, FastAPI, SQLAlchemy
- **База данных**: PostgreSQL с asyncpg
- **Кеширование**: Redis
- **Контейнеризация**: Docker, Docker Compose
- **Миграции**: Alembic
- **Тестирование**: pytest
- **Линтинг**: ruff, mypy
- **Сборка**: uv, hatchling

## Быстрый старт

### Предварительные требования

- Python 3.12+
- Docker и Docker Compose
- uv (рекомендуется) или pip

### Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd antiques
```

2. Установите зависимости:
```bash
# С uv (рекомендуется)
uv sync

# Или с pip
pip install -e .
```

3. Настройте переменные окружения:
```bash
cp .env.template .env
# Отредактируйте .env файл
```

4. Запустите с Docker:
```bash
make dev-setup-docker
make docker-up-dev
```

Или локально:
```bash
# Запустите PostgreSQL и Redis
docker-compose up -d postgres redis

# Примените миграции
make migrate

# Запустите приложение
uv run python -m src.main
```

## API Документация

После запуска приложения документация API доступна по адресам:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Разработка

### Структура проекта

```
src/
├── application/          # Слой приложения
│   ├── dtos/            # Data Transfer Objects
│   ├── interfaces/      # Интерфейсы
│   └── use_cases/       # Use cases
├── config/              # Конфигурация
│   └── ioc/            # Dependency Injection
├── domain/              # Доменный слой
│   ├── entities/        # Сущности
│   ├── services/        # Доменные сервисы
│   └── value_objects/   # Объекты-значения
├── infrastructures/     # Инфраструктурный слой
│   ├── db/             # База данных
│   ├── http/           # HTTP клиенты
│   └── broker/         # Message broker
└── presentation/        # Слой представления
    ├── api/            # REST API
    └── cli/            # CLI интерфейс
```

### Команды разработки

```bash
# Линтинг
make lint

# Форматирование
make format

# Проверка типов
make type-check

# Запуск тестов
make test

# Покрытие тестами
make test-cov

# Все проверки
make check
```

### Docker команды

```bash
# Сборка образов
make docker-build-dev

# Запуск development окружения
make docker-up-dev

# Запуск тестов в Docker
make docker-test

# Миграции
make docker-migrate
```

## Миграции базы данных

```bash
# Создание новой миграции
make migration msg="Описание изменений"

# Применение миграций
make migrate

# Откат миграции
make migrate-downgrade

# История миграций
make migrate-history
```

## Тестирование

```bash
# Запуск всех тестов
make test

# Запуск с покрытием
make test-cov

# Запуск в Docker
make docker-test
```

## Развертывание

### Production

1. Настройте переменные окружения для production
2. Соберите production образ:
```bash
make docker-build
```

3. Запустите с docker-compose:
```bash
docker-compose up -d
```

### Переменные окружения

Основные переменные окружения:
- `DATABASE_URL` - URL подключения к PostgreSQL
- `REDIS_URL` - URL подключения к Redis
- `ENVIRONMENT` - Окружение (development/production)
- `LOG_LEVEL` - Уровень логирования

## Архитектура

Приложение следует принципам Clean Architecture:

- **Domain Layer** - бизнес-логика и правила
- **Application Layer** - use cases и интерфейсы
- **Infrastructure Layer** - внешние зависимости
- **Presentation Layer** - API и CLI
