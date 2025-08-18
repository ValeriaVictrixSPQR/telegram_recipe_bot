#!/bin/bash

# Простой скрипт развертывания Telegram бота без Docker

echo "🚀 Простое развертывание Telegram бота..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен. Устанавливаем..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден. Создаем..."
    echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" > .env
    echo "⚠️  Отредактируйте файл .env и укажите ваш токен бота!"
    exit 1
fi

# Создаем виртуальное окружение
echo "🐍 Создаем виртуальное окружение..."
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt

# Создаем директорию для логов
mkdir -p logs

echo "✅ Установка завершена!"
echo ""
echo "📝 Для запуска бота выполните:"
echo "   source venv/bin/activate"
echo "   python3 bot.py"
echo ""
echo "🔄 Для автозапуска используйте systemd сервис:"
echo "   sudo cp systemd.service /etc/systemd/system/telegram-bot.service"
echo "   sudo systemctl enable telegram-bot"
echo "   sudo systemctl start telegram-bot"
