#!/bin/bash

# Скрипт мониторинга Telegram бота

echo "📊 Мониторинг Telegram бота"
echo "================================"

# Проверяем статус Docker контейнеров
if command -v docker-compose &> /dev/null; then
    echo "🐳 Статус Docker контейнеров:"
    docker-compose ps
    echo ""
    
    echo "📝 Последние логи Docker:"
    docker-compose logs --tail=20
    echo ""
fi

# Проверяем статус systemd сервиса
if systemctl list-unit-files | grep -q telegram-bot; then
    echo "⚙️  Статус systemd сервиса:"
    sudo systemctl status telegram-bot --no-pager -l
    echo ""
fi

# Проверяем использование ресурсов
echo "💾 Использование ресурсов:"
echo "Память:"
free -h
echo ""
echo "Диск:"
df -h
echo ""

# Проверяем сетевые соединения
echo "🌐 Сетевые соединения:"
netstat -tulpn | grep python3 2>/dev/null || echo "Нет активных соединений Python"
echo ""

# Проверяем файлы проекта
echo "📁 Статус файлов проекта:"
ls -la recipes.json .env 2>/dev/null || echo "Некоторые файлы отсутствуют"
echo ""

# Проверяем размер файла с рецептами
if [ -f recipes.json ]; then
    echo "📊 Размер файла recipes.json:"
    ls -lh recipes.json
    echo ""
fi

echo "✅ Мониторинг завершен"
