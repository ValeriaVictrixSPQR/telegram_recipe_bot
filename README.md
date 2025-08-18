# 🍽️ Telegram Bot Рецептов

Telegram бот для получения рецептов детского питания с 90 различными рецептами.

## ✨ Возможности

- 📖 90 рецептов детского питания
- 🥘 Подробные инструкции по приготовлению
- 🎯 Простой и понятный интерфейс
- 🔄 Случайный выбор рецептов
- 📱 Адаптирован для мобильных устройств

## 🚀 Быстрый старт

### Размещение на GitHub

1. **Создайте новый репозиторий на GitHub**
2. **Клонируйте репозиторий:**
```bash
git clone <your-repo-url>
cd telegram_recipe_bot
```

### Локальная разработка

1. **Клонируйте репозиторий:**
```bash
git clone <your-repo-url>
cd telegram_recipe_bot
```

2. **Создайте файл .env:**
```bash
echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" > .env
```

3. **Установите зависимости:**
```bash
pip3 install -r requirements.txt
```

4. **Запустите бота:**
```bash
python3 bot.py
```

### Развертывание на сервере

#### Способ 1: Docker (рекомендуется)

```bash
# Запуск автоматического развертывания
chmod +x deploy.sh
./deploy.sh
```

#### Способ 2: Простое развертывание

```bash
# Запуск простого развертывания
chmod +x deploy_simple.sh
./deploy_simple.sh
```

#### Способ 3: Systemd сервис

```bash
# Копируем сервис файл
sudo cp systemd.service /etc/systemd/system/telegram-bot.service

# Редактируем токен и пути
sudo nano /etc/systemd/system/telegram-bot.service

# Включаем и запускаем
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

## 📋 Структура проекта

```
telegram_recipe_bot/
├── bot.py                 # Основной код бота
├── recipes.json           # База рецептов (90 рецептов)
├── requirements.txt       # Зависимости Python
├── .env                  # Конфигурация (токен бота)
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Docker Compose конфигурация
├── deploy.sh             # Скрипт развертывания с Docker
├── deploy_simple.sh      # Простой скрипт развертывания
├── monitor.sh            # Скрипт мониторинга
├── systemd.service       # Systemd сервис
├── nginx.conf            # Конфигурация Nginx
├── .github/workflows/    # GitHub Actions для CI/CD
├── .gitignore            # Исключения для Git
├── DEPLOYMENT.md         # Подробная инструкция по развертыванию
└── README.md             # Этот файл
```

## 🐳 Docker команды

```bash
# Сборка и запуск
docker-compose up --build -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart
```

## 📊 Мониторинг

```bash
# Запуск мониторинга
chmod +x monitor.sh
./monitor.sh

# Проверка статуса Docker
docker-compose ps

# Проверка статуса systemd
sudo systemctl status telegram-bot
```

## 🔧 Настройка

### Переменные окружения

- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота

### Файл recipes.json

Файл содержит 90 рецептов в формате JSON:
```json
{
  "recipes": [
    {
      "id": 1,
      "name": "Название рецепта",
      "ingredients": "Список ингредиентов",
      "instructions": "Инструкция по приготовлению"
    }
  ]
}
```

## 🚨 Устранение неполадок

### Бот не запускается

1. Проверьте правильность токена в файле .env
2. Убедитесь, что все зависимости установлены
3. Проверьте логи: `docker-compose logs` или `sudo journalctl -u telegram-bot`

### Проблемы с Docker

```bash
# Перезапуск Docker
sudo systemctl restart docker

# Очистка системы
docker system prune -a
```

## 📚 Документация

- [DEPLOYMENT.md](DEPLOYMENT.md) - Подробная инструкция по развертыванию
- [AMVERA_SETUP.md](AMVERA_SETUP.md) - Интеграция с AMVERA через GitHub
- [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) - Размещение на GitHub
- [commands.md](commands.md) - Описание команд бота

## 🔄 CI/CD с GitHub Actions

Проект настроен для автоматического развертывания с помощью GitHub Actions:

- **Автоматическое развертывание** при push в main/master ветку
- **Публикация Docker образа** в Docker Hub
- **Тестирование** перед развертыванием
- **Развертывание на AMVERA** через SSH

### Поддерживаемые платформы

- **Локальный сервер** - через deploy.sh
- **AMVERA** - через GitHub Actions (рекомендуется)
- **Docker Hub** - автоматическая публикация образов

### Настройка GitHub Secrets

Для работы CI/CD добавьте в настройки репозитория (Settings → Secrets and variables → Actions):

#### Для локального сервера:
- `HOST` - IP адрес вашего сервера
- `USERNAME` - имя пользователя на сервере
- `SSH_KEY` - приватный SSH ключ для доступа к серверу
- `PORT` - SSH порт (обычно 22)

#### Для AMVERA:
- `AMVERA_HOST` - IP адрес вашего AMVERA сервера
- `AMVERA_USERNAME` - имя пользователя на AMVERA
- `AMVERA_SSH_KEY` - приватный SSH ключ
- `AMVERA_PORT` - SSH порт (обычно 22)
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота

#### Для Docker Hub:
- `DOCKER_USERNAME` - имя пользователя Docker Hub
- `DOCKER_PASSWORD` - пароль Docker Hub

## 🤝 Поддержка

При возникновении проблем:
1. Проверьте логи
2. Убедитесь в правильности токена
3. Проверьте права доступа к файлам
4. Убедитесь в доступности интернета

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.
