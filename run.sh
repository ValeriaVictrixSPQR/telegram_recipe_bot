#!/bin/bash

echo "🍽️ Запуск Telegram бота рецептов..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

# Проверяем наличие файла .env
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📝 Создайте файл .env с содержимым:"
    echo "TELEGRAM_BOT_TOKEN=your_bot_token_here"
    echo ""
    echo "💡 Скопируйте env_example.txt в .env и отредактируйте"
    exit 1
fi

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

# Запускаем бота
echo "🚀 Запуск бота..."
python3 bot.py
