FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директории для логов и данных
RUN mkdir -p /app/logs /app/data

# Копируем код приложения
COPY web_app.py .
COPY recipes.json .
COPY .env .

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 webuser && chown -R webuser:webuser /app
USER webuser

# Открываем порт
EXPOSE 8000

# Проверяем работоспособность
RUN python3 -c "import flask; print('Flask library imported successfully')"

# Команда запуска (используем gunicorn для продакшена)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "web_app:app"]
