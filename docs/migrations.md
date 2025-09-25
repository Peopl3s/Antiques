# Миграции базы данных

Этот проект использует Alembic для управления миграциями базы данных PostgreSQL.

## Настройка

1. Убедитесь, что PostgreSQL запущен и доступен
2. Создайте базу данных:
   ```sql
   CREATE DATABASE antiques;
   ```
3. Настройте переменную окружения `DATABASE_URL`:
   ```bash
   export DATABASE_URL="postgresql+asyncpg://username:password@localhost/antiques"
   ```

## Команды для работы с миграциями

### Создание новой миграции
```bash
# Создать миграцию с автогенерацией (требует подключения к БД)
make migration msg="Описание изменений"

# Или напрямую через alembic
uv run alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций
```bash
# Применить все ожидающие миграции
make migrate

# Или напрямую
uv run alembic upgrade head
```

### Откат миграций
```bash
# Откатить на одну миграцию назад
make migrate-downgrade

# Или напрямую
uv run alembic downgrade -1
```

### Просмотр истории миграций
```bash
# Показать историю миграций
make migrate-history

# Показать текущую миграцию
make migrate-current
```

### Другие полезные команды
```bash
# Отметить БД как находящуюся на определенной миграции (без применения)
make migrate-stamp

# Показать SQL для миграции (без применения)
uv run alembic upgrade head --sql
```

## Структура файлов

- `alembic.ini` - конфигурация Alembic
- `alembic/env.py` - настройки окружения для миграций
- `alembic/versions/` - директория с файлами миграций
- `alembic/script.py.mako` - шаблон для новых миграций

## Работа с моделями

При изменении моделей в `src/infrastructures/db/models/`:

1. Создайте новую миграцию с автогенерацией
2. Проверьте сгенерированный код миграции
3. При необходимости отредактируйте миграцию вручную
4. Примените миграцию к базе данных

## Примеры

### Создание таблицы
```python
def upgrade() -> None:
    op.create_table(
        'new_table',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('new_table')
```

### Добавление колонки
```python
def upgrade() -> None:
    op.add_column('artifacts', sa.Column('new_field', sa.String(100), nullable=True))

def downgrade() -> None:
    op.drop_column('artifacts', 'new_field')
```

### Создание индекса
```python
def upgrade() -> None:
    op.create_index('ix_table_field', 'table', ['field'])

def downgrade() -> None:
    op.drop_index('ix_table_field', table_name='table')
```
