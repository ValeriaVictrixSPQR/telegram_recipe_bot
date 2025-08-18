FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директории для логов и данных
RUN mkdir -p /app/logs /app/data

# Копируем код приложения
COPY app.py .
COPY recipes.json .
COPY .env .

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Открываем порт
EXPOSE 8000

# Проверяем работоспособность
RUN python3 -c "import telegram; print('Telegram library imported successfully')"

# Команда запуска
CMD ["python3", "app.py"]
