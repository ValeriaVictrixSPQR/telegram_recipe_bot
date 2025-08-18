#!/bin/bash

# Скрипт развертывания Telegram бота на сервере

echo "🚀 Начинаем развертывание Telegram бота..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Устанавливаем..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker установлен. Перезагрузите систему и запустите скрипт снова."
    exit 1
fi

# Проверяем наличие Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Устанавливаем..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose установлен."
fi

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден. Создаем..."
    echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" > .env
    echo "⚠️  Отредактируйте файл .env и укажите ваш токен бота!"
    exit 1
fi

# Создаем директорию для логов
mkdir -p logs

# Останавливаем существующие контейнеры
echo "🛑 Останавливаем существующие контейнеры..."
docker-compose down

# Удаляем старые образы
echo "🧹 Удаляем старые образы..."
docker system prune -f

# Собираем и запускаем
echo "🔨 Собираем и запускаем бота..."
docker-compose up --build -d

# Проверяем статус
echo "📊 Проверяем статус..."
docker-compose ps

echo "✅ Развертывание завершено!"
echo "📝 Логи: docker-compose logs -f"
echo "🛑 Остановка: docker-compose down"
echo "🔄 Перезапуск: docker-compose restart"
