# Используем официальный легковесный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем pyproject.toml и poetry.lock (если есть)
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости (без виртуального окружения внутри контейнера)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем всё приложение внутрь контейнера
COPY . .

# Команда запуска FastAPI через Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]