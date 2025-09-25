# Использование MyPy в проекте Antiques

## Установка

```bash
# Установка dev зависимостей (включая MyPy)
uv sync --dev

# Или установка только MyPy
uv add --dev mypy
```

## Основные команды

### Проверка типов

```bash
# Проверить весь проект
uv run mypy src/

# Проверить конкретный файл
uv run mypy src/main.py

# Проверить с подробным выводом
uv run mypy src/ --show-error-codes

# Проверить с показом контекста ошибок
uv run mypy src/ --show-error-context

# Проверить только определенные модули
uv run mypy src/application/ src/domain/
```

### Использование Makefile

```bash
# Показать все доступные команды
make help

# Проверить типы
make type-check

# Запустить все проверки (lint + format + type check)
make check

# Запустить CI pipeline
make ci
```

## Конфигурация MyPy

Основная конфигурация MyPy находится в `pyproject.toml` в секции `[tool.mypy]`.

### Основные настройки

- **python_version**: Python 3.12
- **strict**: false (мягкая проверка для начала)
- **ignore_missing_imports**: true (игнорировать отсутствующие импорты)
- **warn_return_any**: true (предупреждать о возврате Any)
- **no_implicit_optional**: true (требовать явного Optional)

### Per-module настройки

```toml
# Более мягкие правила для тестов и примеров
[[tool.mypy.overrides]]
module = [
    "tests.*",
    "examples.*",
]
disallow_untyped_defs = false
disallow_incomplete_defs = false
check_untyped_defs = false

# Игнорировать отсутствующие импорты для внешних библиотек
[[tool.mypy.overrides]]
module = [
    "faststream.*",
    "granian.*",
    "structlog.*",
]
ignore_missing_imports = true
```

## Pre-commit интеграция

MyPy автоматически запускается при коммите через pre-commit hooks:

```bash
# Установить pre-commit hooks
pre-commit install

# Запустить hooks на всех файлах
pre-commit run --all-files

# Запустить только mypy
pre-commit run mypy
```

## Типичные ошибки и их исправление

### 1. Union types (None проверки)

```python
# ❌ Ошибка: Item "None" has no attribute
def process_artifact(artifact: ArtifactEntity | None) -> str:
    return artifact.name  # Error!

# ✅ Исправление: проверка на None
def process_artifact(artifact: ArtifactEntity | None) -> str:
    if artifact is None:
        raise ValueError("Artifact is required")
    return artifact.name
```

### 2. Decorators на property

```python
# ❌ Ошибка: Decorators on top of @property are not supported
@property
@computed_field
def database_url(self) -> PostgresDsn:
    return PostgresDsn.build(...)

# ✅ Исправление: убрать @property
@computed_field
def database_url(self) -> PostgresDsn:
    return PostgresDsn.build(...)
```

### 3. Возврат Any

```python
# ❌ Ошибка: Returning Any from function declared to return "str"
def get_id() -> str:
    data = {"id": "123"}
    return data["id"]  # MyPy не знает тип

# ✅ Исправление: явная типизация
def get_id() -> str:
    data: dict[str, str] = {"id": "123"}
    return data["id"]
```

### 4. Неожиданные аргументы

```python
# ❌ Ошибка: Unexpected keyword argument
class MyModel:
    def __init__(self, name: str):
        self.name = name

# MyPy не видит поля класса
model = MyModel(name="test", age=25)  # Error!

# ✅ Исправление: использовать dataclass или TypedDict
from dataclasses import dataclass

@dataclass
class MyModel:
    name: str
    age: int
```

## Постепенное улучшение типизации

### Этап 1: Базовая типизация
```bash
# Начать с мягкой конфигурации
uv run mypy src/ --ignore-missing-imports
```

### Этап 2: Добавление аннотаций
```python
# Добавлять типы постепенно
def process_data(data: dict[str, Any]) -> list[str]:
    return [str(item) for item in data.values()]
```

### Этап 3: Строгая типизация
```toml
# В pyproject.toml
[tool.mypy]
strict = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
```

## Интеграция с IDE

### VS Code

Добавьте в `.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.mypyArgs": [
        "--config-file=pyproject.toml"
    ],
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports.ruff": true
        }
    }
}
```

### PyCharm

1. Включите MyPy в настройках
2. Укажите путь к конфигурации: `pyproject.toml`
3. Включите проверку типов в реальном времени

## CI/CD интеграция

### GitHub Actions

```yaml
name: Type Check

on: [push, pull_request]

jobs:
  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install uv
        uses: astral-sh/setup-uv@v2
      - name: Install dependencies
        run: uv sync --dev
      - name: Run mypy
        run: uv run mypy src/
```

## Полезные флаги

```bash
# Показать коды ошибок
uv run mypy src/ --show-error-codes

# Показать контекст ошибок
uv run mypy src/ --show-error-context

# Показать статистику
uv run mypy src/ --show-error-codes --statistics

# Проверить только измененные файлы
uv run mypy src/ --incremental

# Игнорировать отсутствующие импорты
uv run mypy src/ --ignore-missing-imports

# Строгая проверка
uv run mypy src/ --strict
```

## Решение проблем

### Медленная работа

```bash
# Использовать кэш
uv run mypy src/ --incremental

# Проверять только измененные файлы
uv run mypy src/ --incremental --follow-imports=silent
```

### Слишком много ошибок

```bash
# Начать с мягкой конфигурации
uv run mypy src/ --ignore-missing-imports --no-strict-optional

# Постепенно добавлять строгость
uv run mypy src/ --warn-return-any --warn-unused-configs
```

### Конфликты с другими инструментами

```bash
# Использовать только mypy для проверки типов
uv run mypy src/ --no-error-summary

# Исключить определенные файлы
uv run mypy src/ --exclude "tests/.*"
```

## Лучшие практики

1. **Начните с мягкой конфигурации** и постепенно ужесточайте
2. **Добавляйте типы постепенно** - не пытайтесь исправить все сразу
3. **Используйте `# type: ignore`** только в крайних случаях
4. **Настройте IDE** для автоматической проверки типов
5. **Запускайте mypy в CI** для предотвращения регрессий
6. **Документируйте сложные типы** с помощью комментариев

## Полезные ссылки

- [Официальная документация MyPy](https://mypy.readthedocs.io/)
- [Типы в Python](https://docs.python.org/3/library/typing.html)
- [Typing cheatsheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)

