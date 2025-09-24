# Использование Ruff в проекте Antiques

## Установка

```bash
# Установка dev зависимостей (включая Ruff)
uv sync --dev

# Или установка только Ruff
uv add --dev ruff
```

## Основные команды

### Проверка кода (linting)

```bash
# Проверить весь проект
uv run ruff check src/ tests/

# Проверить конкретный файл
uv run ruff check src/main.py

# Проверить с подробным выводом
uv run ruff check src/ tests/ --verbose

# Проверить только определенные правила
uv run ruff check src/ --select E,F,W

# Игнорировать определенные правила
uv run ruff check src/ --ignore E501,W503
```

### Автоматическое исправление

```bash
# Исправить все автоматически исправляемые проблемы
uv run ruff check --fix src/ tests/

# Исправить только определенные правила
uv run ruff check --fix --select E,F src/

# Показать, что будет исправлено, без фактического исправления
uv run ruff check --fix --diff src/
```

### Форматирование кода

```bash
# Отформатировать весь проект
uv run ruff format src/ tests/

# Проверить форматирование без изменений
uv run ruff format --check src/ tests/

# Показать diff форматирования
uv run ruff format --diff src/
```

### Комплексная проверка

```bash
# Проверить и исправить все проблемы
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/

# Или одной командой (если настроено в pyproject.toml)
uv run ruff check --fix src/ tests/ && uv run ruff format src/ tests/
```

## Использование Makefile

```bash
# Показать все доступные команды
make help

# Установить dev зависимости
make install-dev

# Проверить код
make lint

# Исправить проблемы автоматически
make lint-fix

# Отформатировать код
make format

# Запустить все проверки
make check

# Запустить тесты
make test

# Запустить тесты с покрытием
make test-cov

# Очистить кэш
make clean

# Настроить dev окружение
make dev-setup

# Запустить CI pipeline
make ci
```

## Pre-commit hooks

```bash
# Установить pre-commit hooks
pre-commit install

# Запустить hooks на всех файлах
pre-commit run --all-files

# Обновить hooks
pre-commit autoupdate
```

## Конфигурация

Основная конфигурация Ruff находится в `pyproject.toml` в секции `[tool.ruff]`.

### Основные настройки

- **target-version**: Python 3.12
- **line-length**: 88 символов (как в Black)
- **indent-width**: 4 пробела

### Включенные правила

- **E4, E7, E9**: Критические ошибки pycodestyle
- **F**: Pyflakes (неиспользуемые импорты, переменные)
- **W**: Предупреждения pycodestyle
- **B**: flake8-bugbear (потенциальные баги)
- **C4**: flake8-comprehensions (улучшения списковых включений)
- **UP**: pyupgrade (современный Python синтаксис)
- **ARG**: flake8-unused-arguments (неиспользуемые аргументы)
- **SIM**: flake8-simplify (упрощения кода)
- **TCH**: flake8-type-checking (проверки типов)
- **TID**: flake8-tidy-imports (порядок импортов)
- **Q**: flake8-quotes (кавычки)
- **I**: isort (сортировка импортов)
- **N**: pep8-naming (именование)
- **D**: pydocstyle (документация)
- **S**: flake8-bandit (безопасность)
- **A**: flake8-builtins (встроенные функции)
- **COM**: flake8-commas (запятые)
- **C90**: mccabe (сложность)
- **ICN**: flake8-import-conventions (конвенции импортов)
- **G**: flake8-logging-format (форматирование логов)
- **INP**: flake8-no-pep420 (PEP 420)
- **PIE**: flake8-pie (улучшения)
- **T20**: flake8-print (print statements)
- **PYI**: flake8-pyi (stub files)
- **PT**: flake8-pytest-style (стиль pytest)
- **RSE**: flake8-raise (исключения)
- **RET**: flake8-return (возвраты)
- **SLF**: flake8-self (self)
- **SLOT**: flake8-slots (slots)
- **YTT**: flake8-2020 (Python 2020)

### Игнорируемые правила

- **B027**: Пустые методы в абстрактных классах
- **FBT003**: Булевы позиционные аргументы
- **S105, S106, S107**: Возможные пароли
- **C901, PLR0911, PLR0912, PLR0913, PLR0915**: Сложность
- **PLR2004**: Магические значения
- **T201**: Print statements
- **TID252**: Относительные импорты
- **F403, F401**: Star импорты в __init__.py
- **E501**: Длинные строки

### Per-file ignores

- **tests/**: Разрешает assert, магические значения, относительные импорты
- **examples/**: Разрешает print, магические значения
- **pyproject.toml, setup.py, tox.ini, pytest.ini**: Разрешает магические значения

## Интеграция с IDE

### VS Code

Добавьте в `.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "none",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": true,
            "source.organizeImports.ruff": true
        }
    }
}
```

### PyCharm

1. Установите плагин Ruff
2. Настройте Ruff как внешний инструмент
3. Включите автоисправление при сохранении

## CI/CD интеграция

### GitHub Actions

```yaml
name: Lint and Format Check

on: [push, pull_request]

jobs:
  lint:
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
      - name: Run ruff check
        run: uv run ruff check src/ tests/
      - name: Run ruff format check
        run: uv run ruff format --check src/ tests/
```

## Лучшие практики

1. **Используйте pre-commit hooks** для автоматической проверки
2. **Запускайте `make check`** перед коммитом
3. **Исправляйте проблемы постепенно** - не все сразу
4. **Настройте IDE** для автоматического форматирования
5. **Используйте `--fix`** для автоматических исправлений
6. **Проверяйте diff** перед применением изменений
7. **Настройте CI** для проверки в pull requests

## Решение проблем

### Ruff не находит файлы

```bash
# Убедитесь, что вы в правильной директории
pwd

# Проверьте, что файлы существуют
ls -la src/

# Запустите с verbose для отладки
uv run ruff check --verbose src/
```

### Конфликты с другими линтерами

```bash
# Отключите другие линтеры в IDE
# Используйте только Ruff для форматирования и линтинга
```

### Медленная работа

```bash
# Используйте кэш
uv run ruff check --cache src/

# Проверяйте только измененные файлы
uv run ruff check --diff src/
```

## Полезные ссылки

- [Официальная документация Ruff](https://docs.astral.sh/ruff/)
- [Правила Ruff](https://docs.astral.sh/ruff/rules/)
- [Конфигурация Ruff](https://docs.astral.sh/ruff/configuration/)
- [Pre-commit hooks](https://pre-commit.com/)
