from src.domain.entities.artifact import ArtifactEntity<div align="center">

# 🏛️ Антиквариум API

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.117+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-24+-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Современное API для управления коллекцией артефактов в музее антиквариата**

</div>

---

## 📖 Описание проекта

**Антиквариум API** — это элегантное и масштабируемое веб-приложение, разработанное для эффективного управления коллекциями музейных артефактов. Система построена с использованием современных архитектурных паттернов и передовых технологий, обеспечивая высокую производительность, надежность и удобство в эксплуатации.

### 🎯 Ключевые особенности

- 🏗️ **Чистая архитектура** (Clean Architecture) с четким разделением ответственности
- ⚡ **Высокая производительность** благодаря асинхронной обработке запросов
- 🧠 **Интеллектуальное кеширование** с Redis для оптимизации скорости работы
- 🗄️ **Надежное хранение данных** в PostgreSQL с поддержкой транзакций
- 🐳 **Контейнеризация** с Docker для простой развертывания и масштабирования
- 📊 **Автоматическая документация** API с Swagger UI и ReDoc
- 🔒 **Строгая валидация** данных с использованием Pydantic
- 🧪 **Комплексное тестирование** pytest с высоким покрытием кода

---


## 🛠️ Технологический стек

### 🎨 Backend
- **Язык**: Python 3.12+ с современными возможностями
- **Фреймворк**: FastAPI для высокопроизводительных API
- **ORM**: SQLAlchemy 2.0 с асинхронной поддержкой
- **Валидация**: Pydantic для строгой проверки данных
- **DI-контейнер**: Dishka для управления зависимостями

### 🗄️ База данных
- **Основная СУБД**: PostgreSQL 16+ с asyncpg
- **Миграции**: Alembic для управления схемой базы данных
- **Кеширование**: Redis 7+ для оптимизации производительности

### 🐳 Инфраструктура
- **Контейнеризация**: Docker и Docker Compose
- **Веб-сервер**: Uvicorn с поддержкой HTTP/2
- **Асинхронность**: Full async/await поддержка

### 🧪 Разработка и тестирование
- **Тестирование**: pytest с поддержкой асинхронных тестов
- **Линтинг**: ruff для быстрой проверки кода
- **Типизация**: mypy для статической проверки типов
- **Форматирование**: автоматическое форматирование кода
- **Pre-commit**: хуки для контроля качества кода

---

## 🏁 Быстрый старт

### 📋 Предварительные требования

- Python 3.12+
- Docker и Docker Compose
- uv (рекомендуется) или pip

### 🚀 Установка и запуск

#### 1. Клонирование репозитория
```bash
git clone https://github.com/Peopl3s/Antiques.git
cd Antiques
```

#### 2. Установка зависимостей
```bash
# Рекомендуемый способ с uv
uv sync

# Альтернативный способ с pip
pip install -e .
```

#### 3. Настройка окружения
```bash
cp .env.template .env
# Отредактируйте .env файл с вашими настройками
```

#### 4. Запуск с Docker (рекомендуется)
```bash
# Полная настройка development окружения
make dev-setup-docker

# Запуск приложения
make docker-up-dev
```

#### 5. Локальный запуск
```bash
# Запуск зависимостей
docker-compose up -d postgres redis

# Применение миграций
make migrate

# Запуск приложения
uv run python -m src.main
```

---

## 📚 Документация API

После запуска приложения документация доступна по следующим адресам:

### 🎯 Swagger UI
```
http://localhost:8000/api/docs
```
Интерактивная документация с возможностью тестирования API прямо в браузере.

### 📖 ReDoc
```
http://localhost:8000/api/redoc
```
Стилизованная документация с трехпанельной навигацией.

### 📄 OpenAPI Schema
```
http://localhost:8000/api/openapi.json
```
Спецификация API в формате OpenAPI 3.0.

---

## 🏗️ Архитектура проекта

Приложение следует принципам **Clean Architecture**, обеспечивая четкое разделение ответственности, независимость слоев и тестируемость. Архитектура построена вокруг бизнес-логики, которая изолирована от внешних зависимостей, таких как базы данных, фреймворки и другие инфраструктурные компоненты.

### 📐 Общая схема архитектуры

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│                   (Слой представления)                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │   REST API      │  │      CLI        │  │   GraphQL?      ││
│  │  (FastAPI)      │  │                 │  │                 ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│                     (Слой приложения)                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │    Use Cases    │  │      DTOs       │  │   Interfaces    ││
│  │ (Бизнес-правила)│  │  (Передача      │  │    (Порты)      ││
│  │                 │  │   данных)       │  │                 ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                           │
│                   (Доменный слой)                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │    Entities     │  │  Value Objects  │  │   Services      ││
│  │   (Сущности)    │  │(Объекты-значения)│  │ (Доменные       ││
│  │                 │  │                 │  │   сервисы)      ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                       │
│                (Инфраструктурный слой)                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │   Databases     │  │      Cache      │  │ Message Brokers││
│  │ (PostgreSQL,    │  │    (Redis)      │  │                 ││
│  │   SQLAlchemy)   │  │                 │  │                 ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 📁 Структура проекта

Ниже представлено детальное дерево каталогов проекта, отражающее архитектурную структуру:

```
.
├── 📁 src/                          # Исходный код приложения
│   ├── 📁 domain/                   # Доменный слой (бизнес-логика)
│   │   ├── 📁 entities/             # Сущности предметной области
│   │   │   └── artifact.py          # Сущность "Артефакт"
│   │   ├── 📁 services/             # Доменные сервисы
│   │   ├── 📁 value_objects/        # Объекты-значения
│   │   │   ├── era.py               # Объект-значение "Эпоха"
│   │   │   └── material.py          # Объект-значение "Материал"
│   │   ├── exceptions.py            # Доменные исключения
│   │   └── __init__.py
│   │
│   ├── 📁 application/              # Слой приложения
│   │   ├── 📁 dtos/                 # Data Transfer Objects
│   │   │   └── artifact.py          # DTO для "Артефакта"
│   │   ├── 📁 interfaces/           # Интерфейсы (порты)
│   │   │   ├── cache.py             # Интерфейс кеширования
│   │   │   ├── http_clients.py      # Интерфейсы HTTP-клиентов
│   │   │   ├── mappers.py           # Интерфейсы мапперов
│   │   │   ├── message_broker.py    # Интерфейс брокера сообщений
│   │   │   └── repositories.py      # Интерфейсы репозиториев
│   │   ├── 📁 use_cases/            # Use cases (интеракторы)
│   │   │   └── get_artifact.py      # Use case "Получить артефакт"
│   │   ├── exceptions.py            # Исключения приложения
│   │   ├── mappers.py               # Мапперы данных
│   │   └── __init__.py
│   │
│   ├── 📁 presentation/             # Слой представления
│   │   ├── 📁 api/                  # API
│   │   │   └── 📁 rest/             # REST API
│   │   │       ├── 📁 v1/           # Версия API v1
│   │   │       │   ├── 📁 controllers/ # Контроллеры
│   │   │       │   │   └── artifact_controller.py
│   │   │       │   ├── exceptions.py   # Обработчики исключений API
│   │   │       │   └── routers.py      # Маршрутизатор
│   │   │       └── middlewares.py   # Промежуточные слои
│   │   └── 📁 cli/                  # CLI интерфейс
│   │   └── __init__.py
│   │
│   ├── 📁 infrastructures/          # Инфраструктурный слой
│   │   ├── 📁 broker/               # Message broker
│   │   │   └── publisher.py         # Публикатор сообщений
│   │   ├── 📁 cache/                # Кеширование
│   │   │   └── redis_client.py      # Redis клиент
│   │   ├── 📁 db/                   # Работа с базой данных
│   │   │   ├── 📁 models/           # ORM модели
│   │   │   │   └── artifact.py      # Модель "Артефакт"
│   │   │   ├── 📁 repositories/     # Репозитории
│   │   │   │   └── artifact.py      # Репозиторий "Артефакт"
│   │   │   ├── exceptions.py        # Исключения БД
│   │   │   ├── session.py           # Управление сессиями БД
│   │   │   └── __init__.py
│   │   ├── 📁 http/                 # HTTP клиенты
│   │   │   └── clients.py           # Реализация HTTP клиентов
│   │   └── __init__.py
│   │
│   └── 📁 config/                   # Конфигурация
│       ├── 📁 ioc/                  # Dependency Injection
│       │   ├── di.py                # Настройка DI-контейнера
│       │   └── providers.py         # Поставщики зависимостей
│       ├── base.py                  # Базовая конфигурация
│       ├── logging.py               # Конфигурация логирования
│       └── __init__.py
│
├── 📁 tests/                        # Тесты
│   ├── 📁 test_application/         # Тесты слоя приложения
│   │   └── 📁 test_use_cases/       # Тесты Use Cases
│   ├── 📁 test_domain/              # Тесты доменного слоя
│   │   ├── 📁 test_entities/        # Тесты сущностей
│   │   └── 📁 test_value_objects/   # Тесты объектов-значений
│   ├── 📁 test_infrastructure/      # Тесты инфраструктурного слоя
│   │   ├── 📁 test_cache/           # Тесты кеширования
│   │   └── 📁 test_db/              # Тесты работы с БД
│   │       ├── 📁 test_models/      # Тесты ORM моделей
│   │       └── 📁 test_repositories/ # Тесты репозиториев
│   ├── 📁 test_presentation/        # Тесты слоя представления
│   │   └── 📁 test_api/             # Тесты API
│   │       └── 📁 test_controllers/ # Тесты контроллеров
│   ├── 📁 test_integration/         # Интеграционные тесты
│   ├── conftest.py                  # Фикстуры pytest
│   └── __init__.py
│
├── 📁 alembic/                      # Миграции базы данных
│   ├── versions/                    # Файлы миграций
│   ├── env.py                       # Окружение Alembic
│   └── script.py.mako               # Шаблон для миграций
│
├── 📁 docs/                         # Документация
│   ├── caching.md                   # Документация по кешированию
│   ├── docker.md                    # Документация по Docker
│   ├── environment.md               # Настройка окружения
│   ├── migrations.md                # Работа с миграциями
│   ├── mypy-usage.md                # Использование MyPy
│   └── ruff-usage.md                # Использование Ruff
│
├── 📁 scripts/                      # Вспомогательные скрипты
│   ├── init-db.sql                  # Скрипт инициализации БД
│   ├── migrate.sh                   # Скрипт миграций
│   └── setup-env.sh                 # Скрипт настройки окружения
│
├── .dockerignore                    # Исключения для Docker
├── .git-commit-template             # Шаблон коммита
├── .gitignore                       # Исключения для Git
├── .pre-commit-config.yaml          # Конфигурация pre-commit
├── .python-version                  # Версия Python
├── alembic.ini                      # Конфигурация Alembic
├── docker-compose.yml               # Docker Compose
├── docker-compose.override.yml      # Переопределение Docker Compose
├── Dockerfile                       # Dockerfile
├── env.template                     # Шаблон файла окружения
├── LICENSE                          # Лицензия
├── Makefile                         # Makefile с командами
├── pyproject.toml                   # Конфигурация проекта и зависимостей
├── README.md                        # Документация проекта
└── uv.lock                          # Lock-файл зависимостей uv
```

### 🎯 Domain Layer (Доменный слой)

**Назначение**: Ядро приложения, содержит бизнес-логику и сущности предметной области. Этот слой не зависит от других слоев и внешних технологий.

**Ключевые компоненты**:
- **`entities/`**: Основные сущности бизнес-модели (например, `Artifact`).
  - Определяют структуру и поведение ключевых объектов.
  - Содержат бизнес-правила и валидацию.
  - Пример: `src/domain/entities/artifact.py`
- **`value_objects/`**: Объекты-значения, представляющие собой неизменяемые типы данных.
  - Инкапсулируют логику, связанную с конкретными значениями (например, `Era`, `Material`).
  - Обеспечивают строгую типизацию и валидацию.
  - Примеры: `src/domain/value_objects/era.py`, `src/domain/value_objects/material.py`
- **`services/`**: Доменные сервисы, реализующие сложную бизнес-логику, которая не относится к одной сущности.
  - Координируют взаимодействие между несколькими сущностями или объектами-значениями.
- **`exceptions.py`**: Специфические для домена исключения.

**Принципы**:
- **Независимость**: Полностью изолирован от фреймворков, баз данных и UI.
- **Чистота**: Содержит только бизнес-логику, без технических деталей.

### 📋 Application Layer (Слой приложения)

**Назначение**: Оркеструет работу доменного слоя для выполнения конкретных задач приложения (use cases). Определяет интерфейсы для взаимодействия с инфраструктурой.

**Ключевые компоненты**:
- **`use_cases/`**: Use cases (случаи использования) или интеракторы.
  - Реализуют конкретные сценарии использования системы (например, `GetArtifact`).
  - Координируют поток данных между сущностями и инфраструктурой.
  - Пример: `src/application/use_cases/get_artifact.py`
- **`dtos/`**: Data Transfer Objects (объекты передачи данных).
  - Используются для передачи данных между слоями, особенно в API.
  - Пример: `src/application/dtos/artifact.py`
- **`interfaces/`**: Интерфейсы (порты), которые определяют контракты для инфраструктурных реализаций.
  - `repositories.py`: Определяет интерфейсы для доступа к данным (например, `ArtifactRepository`).
  - `cache.py`: Определяет интерфейсы для кеширования.
  - `message_broker.py`: Определяет интерфейсы для работы с брокерами сообщений.
  - `http_clients.py`: Определяет интерфейсы для внешних HTTP-вызовов.
- **`mappers.py`**: Объекты для преобразования данных между сущностями домена и DTO/моделями БД.
- **`exceptions.py`**: Исключения уровня приложения.

**Принципы**:
- **Оркестрация**: Не содержит бизнес-логики, а только управляет её выполнением.
- **Зависимости**: Зависит только от доменного слоя и от абстракций (интерфейсов) инфраструктурного слоя.

### 🌐 Presentation Layer (Слой представления)

**Назначение**: Отвечает за взаимодействие с внешним миром: обработку HTTP-запросов, отображение данных, CLI-интерфейсы.

**Ключевые компоненты**:
- **`api/`**: Реализация REST API.
  - `rest/v1/controllers/`: Контроллеры, обрабатывающие входящие HTTP-запросы. Они вызывают соответствующие use cases из application слоя.
    - Пример: `src/presentation/api/rest/v1/controllers/artifact_controller.py`
  - `rest/v1/routers.py`: Определяет маршруты (endpoints) API.
  - `rest/v1/exceptions.py`: Обработчики исключений для HTTP-ответов.
  - `rest/middlewares.py`: Промежуточные слои для обработки запросов (логирование, аутентификация и т.д.).
- **`cli/`**: Командно-строчный интерфейс для управления приложением (если применимо).

**Принципы**:
- **Тонкость**: Содержит минимум логики, в основном делегируя задачи application слою.
- **Адаптация**: Преобразует данные из формата, понятного клиенту (JSON), в DTO для application слоя.

### 🔧 Infrastructure Layer (Инфраструктурный слой)

**Назначение**: Содержит конкретные реализации технологий: базы данных, кеши, внешние API и т.д. Этот слой реализует интерфейсы, определенные в application слое.

**Ключевые компоненты**:
- **`db/`**: Работа с базами данных.
  - `models/`: ORM-модели (SQLAlchemy), представляющие таблицы в базе данных.
    - Пример: `src/infrastructures/db/models/artifact.py`
  - `repositories/`: Реализации репозиториев для доступа к данным. Они реализуют интерфейсы из `application/interfaces/repositories.py`.
    - Пример: `src/infrastructures/db/repositories/artifact.py`
  - `session.py`: Управление сессиями базы данных.
  - `exceptions.py`: Специфические для БД исключения.
- **`cache/`**: Реализация кеширования.
  - `redis_client.py`: Конкретная реализация кеширования с использованием Redis, реализующая интерфейс `application/interfaces/cache.py`.
- **`http/`**: HTTP-клиенты для взаимодействия с внешними сервисами.
  - `clients.py`: Реализации клиентов, реализующие `application/interfaces/http_clients.py`.
- **`broker/`**: Работа с брокерами сообщений (RabbitMQ, Kafka и т.д.).
  - `publisher.py`: Реализация публикации сообщений.

**Принципы**:
- **Реализация**: Содержит "грязную" работу по взаимодействию с внешними системами.
- **Зависимость**: Зависит от application слоя (реализует его интерфейсы) и может зависеть от domain слоя (например, для маппинга данных).

### ⚙️ Config Layer (Слой конфигурации)

**Назначение**: Управление конфигурацией приложения и зависимостями (Dependency Injection).

**Ключевые компоненты**:
- **`ioc/` (Inversion of Control)**: Контейнер зависимостей.
  - `di.py`: Настройка и сборка DI-контейнера (используется библиотека `dishka`).
  - `providers.py`: Поставщики зависимостей, которые "сообщают" контейнеру, как создавать экземпляры классов (например, какая реализация `ArtifactRepository` будет использоваться).
- **`base.py`**: Базовые настройки и конфигурация приложения (чтение `.env`, параметры логирования и т.д.).
- **`logging.py`**: Конфигурация системы логирования.

### 🔄 Поток данных в приложении (на примере GET /api/v1/artifacts/{id})

1. **Presentation Layer**: Запрос поступает в `ArtifactController`.
2. **Controller** вызывает соответствующий **Use Case** из `Application Layer`, передавая ему DTO с данными запроса.
3. **Use Case**:
   a. Запрашивает у **DI-контейнера** необходимую реализацию `ArtifactRepository` (интерфейс из Application Layer, реализация из Infrastructure Layer).
   b. Вызывает метод `get_by_id()` у репозитория.
4. **Repository (Infrastructure Layer)**:
   a. Выполняет запрос к **PostgreSQL** с помощью **SQLAlchemy**.
   b. Преобразует результат запроса (ORM-модель) в доменную сущность `Artifact` (Domain Layer).
   c. Возвращает сущность Use Case'у.
5. **Use Case**:
   a. Выполняет дополнительную бизнес-логику (если требуется).
   b. Преобразует доменную сущность `Artifact` в `ArtifactDTO` (Application Layer).
   c. Возвращает DTO в **Controller**.
6. **Controller (Presentation Layer)**:
   a. Сериализует `ArtifactDTO` в JSON.
   b. Отправляет HTTP-ответ клиенту.

### 🔄 Принципы архитектуры

1.  **Dependency Rule (Правило зависимостей)**:
    - Исходный код зависимостей может указывать только внутрь.
    - Внутренние слои (Domain) не должны ничего знать о внешних слоях (Infrastructure, Presentation).
    - Зависимости реализуются через абстракции (интерфейсы), определенные во внутренних слоях.

2.  **Single Responsibility Principle (Принцип единственной ответственности)**:
    - Каждый модуль, класс, функция имеют одну и только одну причину для изменения.

3.  **Open/Closed Principle (Принцип открытости/закрытости)**:
    - Программные сущности (классы, модули, функции) должны быть открыты для расширения, но закрыты для изменения.
    - Например, чтобы добавить новый способ хранения данных (например, MongoDB), мы создаем новую реализацию репозитория в Infrastructure Layer, не меняя код в Application или Domain слоях.

4.  **Inversion of Control (Инверсия управления)**:
    - Управление зависимостями передается внешнему контейнеру (DI-контейнеру).
    - Компоненты не создают свои зависимости самостоятельно, а получают их "извне".

5.  **Testability (Тестируемость)**:
    - Благодаря использованию интерфейсов и DI, все компоненты легко поддаются модульному тестированием путем подмены реальных зависимостей на моки (mocks) и стабы (stubs).

---

## 🚀 Потенциальные улучшения архитектуры

### 🔄 Unit of Work (Единица работы)

**Что это?**
**Unit of Work (UoW)** — это паттерн проектирования, который отслеживает список бизнес-объектов, измененных в ходе транзакции, и координирует запись изменений и решение проблем параллелизма. По сути, это "список дел" для базы данных, который гарантирует, что все операции в рамках одной бизнес-транзакции будут выполнены как единое целое.

**Как это могло бы быть реализовано в проекте:**

1.  **Интерфейс `UnitOfWorkProtocol`**:
    - Определяется в `src/application/interfaces/uow.py`.
    - Содержал бы методы для управления репозиториями и транзакциями:
        ```python
        from typing import Protocol

        class UnitOfWorkProtocol(Protocol):
            artifacts: ArtifactRepositoryProtocol

            async def __aenter__(self): ...

            async def __aexit__(self, exc_type, exc_val, exc_tb): ...

            async def commit(self): ...

            async def rollback(self): ...
        ```

2.  **Реализация `SqlAlchemyUnitOfWork`**:
    - Располагалась бы в `src/infrastructures/db/uow.py`.
    - Управляла бы сессией SQLAlchemy и предоставляла доступ к репозиториям:
        ```python

        @dataclass(frozen=True, slots=True, kw_only=True)
        class SqlAlchemyUnitOfWork(UnitOfWorkProtocol):
           session: AsyncSession
           artifact_repository = ArtifactRepositorySQLAlchemy

            async def __aenter__(self):
                self.artifacts = self.artifact_repository(session=self.session)
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    await self.commit()
                else:
                    await self.rollback()
                await self._session.close()

            async def commit(self):
                if self.session:
                    await self.ssession.commit()

            async def rollback(self):
                if self.session:
                    await self.session.rollback()
        ```

3.  **Использование в Use Cases**:
    - Use cases получали бы `UnitOfWorkProtocol` через DI и использовали его как контекстный менеджер:
        ```python
        # src/application/use_cases/create_artifact.py
        @dataclass(frozen=True, slots=True, kw_only=True)
        class CreateArtifact:
            uow: UnitOfWorkProtocol

            async def execute(self, data: CreateArtifactDTO) -> ArtifactEntity:
                # Логика создания сущности Artifact из DTO
                new_artifact = Artifact(...)
                async with self.uow:
                    self.uow.artifacts.add(new_artifact)
                    # Можно выполнять операции с другими репозиториями в той же транзакции
                    # self.uow.another_repo.do_something()
                    await self.uow.commit() # Явный коммит (или неявный при выходе из async with)
                return new_artifact
        ```

**Преимущества внедрения UoW:**
- **Атомарность**: Гарантирует, что несколько операций с БД (например, обновление артефакта и логирование этого действия) будут выполнены в одной транзакции.
- **Согласованность**: Предотвращает сохранение частично измененных данных.
- **Упрощение логики**: Use case не должен вручную управлять сессией и транзакциями, он просто работает с репозиториями в рамках UoW.

### 🧩 Aggregates (Агрегаты)

**Что это?**
**Агрегат** — это паттерн из Domain-Driven Design (DDD), представляющий собой кластер связанных объектов-сущностей и объектов-значений, который рассматривается как единое целое. Каждый агрегат имеет корень (Aggregate Root) — сущность, которая является единственной точкой входа для доступа к любому объекту внутри агрегата. Корень агрегата отвечает за обеспечение целостности и инвариантов всего агрегата.

**Как это могло бы быть реализовано в проекте:**

1.  **Определение агрегата**:
    - Предположим, у нас есть сущность `Artifact` (Артефакт) и связанная с ней сущность `RestorationRecord` (Запись о реставрации). `Artifact` может быть корнем агрегата, а `RestorationRecord` — частью этого агрегата.
    - `Artifact` (корень) будет управлять жизненным циклом `RestorationRecord`.

2.  **Структура агрегата в коде**:
    - **Корень агрегата (`Artifact`)**:
        ```python
        # src/domain/entities/artifact.py
        from dataclasses import dataclass, field
        from typing import List
        from .restoration_record import RestorationRecord # Предполагаем, что такая сущность есть

        @dataclass
        class Artifact:
            id: int
            name: str
            # ... другие поля
            restoration_history: List[RestorationRecord] = field(default_factory=list)

            def add_restoration_record(self, record: RestorationRecord):
                """Метод для добавления записи о реставрации с проверкой инвариантов."""
                # Пример инварианта: нельзя добавить запись о будущей реставрации
                if record.date > datetime.now():
                    raise ValueError("Restoration date cannot be in the future")
                self.restoration_history.append(record)

            # ... другие методы, управляющие состоянием агрегата
        ```
    - **Часть агрегата (`RestorationRecord`)**:
        ```python
        # src/domain/entities/restoration_record.py
        from dataclasses import dataclass
        from datetime import date

        @dataclass
        class RestorationRecord:
            id: int
            artifact_id: int # Внешний ключ, но внутри агрегата доступ через корень
            description: str
            date: date
            # ... другие поля
        ```
    - **Важно**: Внешний код не должен напрямую изменять `restoration_history` или создавать `RestorationRecord` без участия `Artifact`. Все операции идут через корень.

3.  **Репозиторий для агрегата**:
    - Репозиторий создается только для корня агрегата (`ArtifactRepository`).
    - Он отвечает за загрузку и сохранение всего агрегата целиком:
        ```python
        # src/infrastructures/db/repositories/artifact.py
        async def get_by_id(self, artifact_id: int) -> Artifact | None:
            # Логика загрузки Artifact из БД
            # И последующей загрузки всех связанных RestorationRecord
            # и сборки объекта агрегата
            pass
        ```

4.  **Использование в Use Cases**:
    - Use case работает с агрегатом через его корень:
        ```python
        # src/application/use_cases/add_restoration_record.py
        @dataclass(frozen=True, slots=True, kw_only=True)
        class AddRestorationRecord:
            uow: UnitOfWorkProtocol

            async def execute(self, artifact_id: int, data: AddRestorationRecordDTO):
                async with self.uow:
                    artifact = await self.uow.artifacts.get_by_id(artifact_id)
                    if not artifact:
                        raise ValueError("Artifact not found")

                    new_record = RestorationRecord(
                        id=None, # Будет сгенерировано БД
                        artifact_id=artifact_id,
                        description=data.description,
                        date=data.date
                    )
                    # Вся логика и валидация инкапсулирована в корне агрегата
                    artifact.add_restoration_record(new_record)

                    # Репозиторий сохраняет весь агрегат
                    await self.uow.artifacts.update(artifact)
                    await self.uow.commit()
        ```

**Преимущества внедрения Агрегатов:**
- **Инкапсуляция бизнес-логики**: Сложные правила и инварианты, связанные с группой объектов, находятся в одном месте (в корне агрегата).
- **Гарантия целостности данных**: Корень агрегата обеспечивает, что его части всегда находились в согласованном состоянии.
- **Упрощение модели предметной области**: Четкие границы агрегатов делают модель более понятной и управляемой.
- **Транзакционная согласованность**: Aggregate Root является естественной границей транзакции (часто в связке с Unit of Work).

---

## 🛠️ Команды разработки

### 🧹 Качество кода
```bash
# Проверка кода
make lint                    # Проверка стиля кода
make lint-fix               # Автоисправление проблем
make format                 # Форматирование кода
make type-check             # Проверка типов
make check                  # Все проверки сразу
```

### 🧪 Тестирование
```bash
# Запуск тестов
make test                   # Базовый запуск тестов
make test-cov               # С покрытием кода
make docker-test            # В Docker окружении
```

### 🗄️ Работа с базой данных
```bash
# Миграции
make migration msg="Описание"  # Создание миграции
make migrate                  # Применение миграций
make migrate-downgrade        # Откат миграции
make migrate-history          # История миграций
```

### 🐳 Docker команды
```bash
# Управление контейнерами
make docker-build            # Сборка production образа
make docker-up-dev           # Запуск development окружения
make docker-down             # Остановка всех сервисов
make docker-logs             # Просмотр логов
make docker-shell            # Shell в контейнере
```

---

## 📊 Примеры использования



### 📖 Получение информации об артефакте
```bash
curl "http://localhost:8001/api/v1/artifacts/{inventory_id}"
```

---

## 🚀 Развертывание

### 🏭 Development развертывание

1. **Настройка окружения**
```bash
cp .env.template .env
# Настройте production параметры
```

2. **Сборка и запуск**
```bash
# Сборка dev образа
make docker-build-dev

# Запуск в dev режиме
make docker-dev
```

---

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста, ознакомьтесь с нашими правилами:

### 📋 Процесс внесения изменений

1. **Форкните репозиторий**
2. **Создайте ветку** для вашей функции (`git checkout -b feature/amazing-feature`)
3. **Внесите изменения** и следуйте стандартам кода
4. **Запустите тесты** (`make lint && make docker-test`)
5. **Создайте коммит** (`git commit -m 'Add amazing feature'`)
6. **Отправьте изменения** (`git push origin feature/amazing-feature`)
7. **Создайте Pull Request**

### 📝 Требования к коду

- Следуйте PEP 8 и нашим правилам линтинга
- Пишите тесты для новой функциональности
- Обновляйте документацию при необходимости
- Используйте осмысленные сообщения коммитов

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---

## 🙏 Благодарности

- Команде **FastAPI** за отличный фреймворк
- Сообществу **Python** за вдохновение
- Всем контрибьюторам, внесшим вклад в развитие проекта

---

## 📞 Контакты

Если у вас есть вопросы или предложения, пожалуйста:

- 📧 Создайте Issue в репозитории
- 💬 Обсудите в Discussions
- 📧 Свяжитесь с разработчиками

---

<div align="center">

**Сделано с ❤️ для мира антиквариата**

[⬆️ Наверх](#-антиквариум-api)

</div>
