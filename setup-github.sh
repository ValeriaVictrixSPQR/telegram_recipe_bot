#!/bin/bash

echo "🚀 Настройка Git репозитория для GitHub..."

# Проверка наличия Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите Git и повторите попытку."
    exit 1
fi

# Инициализация Git репозитория
if [ ! -d ".git" ]; then
    echo "📁 Инициализация Git репозитория..."
    git init
else
    echo "✅ Git репозиторий уже инициализирован"
fi

# Добавление всех файлов
echo "📝 Добавление файлов в Git..."
git add .

# Первый коммит
echo "💾 Создание первого коммита..."
git commit -m "Initial commit: Telegram Recipe Bot"

echo ""
echo "✅ Git репозиторий настроен!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Создайте новый репозиторий на GitHub"
echo "2. Добавьте удаленный репозиторий:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "3. Загрузите код:"
echo "   git push -u origin main"
echo ""
echo "🔑 Для настройки CI/CD добавьте в GitHub Secrets:"
echo "   - HOST (IP вашего сервера)"
echo "   - USERNAME (имя пользователя на сервере)"
echo "   - SSH_KEY (приватный SSH ключ)"
echo "   - PORT (SSH порт, обычно 22)"
echo "   - DOCKER_USERNAME (имя пользователя Docker Hub)"
echo "   - DOCKER_PASSWORD (пароль Docker Hub)"
echo ""
echo "📚 Подробная инструкция в файле server-setup.md"
