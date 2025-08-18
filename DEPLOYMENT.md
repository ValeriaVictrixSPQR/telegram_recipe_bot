# 🚀 Инструкция по развертыванию Telegram бота на сервере

## 📋 Требования к серверу

- **ОС**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **RAM**: минимум 512 MB
- **Диск**: минимум 1 GB свободного места
- **Python**: 3.11+
- **Docker**: 20.10+ (опционально)

## 🔧 Способ 1: Развертывание с Docker (рекомендуется)

### 1. Подготовка сервера

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем необходимые пакеты
sudo apt install -y curl git python3 python3-pip python3-venv
```

### 2. Клонирование проекта

```bash
# Клонируем репозиторий
git clone <your-repo-url>
cd telegram_recipe_bot

# Создаем .env файл
echo "TELEGRAM_BOT_TOKEN=your_actual_token_here" > .env
```

### 3. Запуск с Docker

```bash
# Делаем скрипт исполняемым
chmod +x deploy.sh

# Запускаем развертывание
./deploy.sh
```

### 4. Проверка работы

```bash
# Проверяем статус контейнеров
docker-compose ps

# Смотрим логи
docker-compose logs -f

# Останавливаем бота
docker-compose down
```

## 🔧 Способ 2: Развертывание без Docker

### 1. Создание пользователя

```bash
# Создаем пользователя для бота
sudo useradd -m -s /bin/bash botuser
sudo usermod -aG sudo botuser

# Переключаемся на пользователя
sudo su - botuser
```

### 2. Установка зависимостей

```bash
# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 3. Настройка systemd сервиса

```bash
# Копируем сервис файл
sudo cp systemd.service /etc/systemd/system/telegram-bot.service

# Редактируем токен и пути
sudo nano /etc/systemd/system/telegram-bot.service

# Перезагружаем systemd
sudo systemctl daemon-reload

# Включаем автозапуск
sudo systemctl enable telegram-bot

# Запускаем сервис
sudo systemctl start telegram-bot

# Проверяем статус
sudo systemctl status telegram-bot
```

## 🔧 Способ 3: Развертывание с Nginx (для продакшена)

### 1. Установка Nginx

```bash
sudo apt install -y nginx
```

### 2. Настройка конфигурации

```bash
# Копируем конфигурацию
sudo cp nginx.conf /etc/nginx/sites-available/telegram-bot

# Создаем символическую ссылку
sudo ln -s /etc/nginx/sites-available/telegram-bot /etc/nginx/sites-enabled/

# Проверяем конфигурацию
sudo nginx -t

# Перезапускаем Nginx
sudo systemctl restart nginx
```

### 3. Настройка SSL (Let's Encrypt)

```bash
# Устанавливаем Certbot
sudo apt install -y certbot python3-certbot-nginx

# Получаем SSL сертификат
sudo certbot --nginx -d your-domain.com

# Проверяем автообновление
sudo certbot renew --dry-run
```

## 📊 Мониторинг и логирование

### Просмотр логов

```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u telegram-bot -f

# Файловые логи
tail -f logs/bot.log
```

### Мониторинг ресурсов

```bash
# Использование памяти
htop

# Дисковое пространство
df -h

# Сетевые соединения
netstat -tulpn
```

## 🔒 Безопасность

### 1. Firewall

```bash
# Открываем только необходимые порты
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. Обновления

```bash
# Автоматические обновления безопасности
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 🚨 Устранение неполадок

### Бот не запускается

```bash
# Проверяем логи
docker-compose logs
sudo journalctl -u telegram-bot

# Проверяем токен
cat .env

# Проверяем права доступа
ls -la
```

### Проблемы с Docker

```bash
# Перезапуск Docker
sudo systemctl restart docker

# Очистка системы
docker system prune -a

# Проверка статуса
docker info
```

## 📝 Полезные команды

```bash
# Перезапуск бота
docker-compose restart
sudo systemctl restart telegram-bot

# Обновление кода
git pull
docker-compose up --build -d

# Резервное копирование
cp recipes.json recipes_backup_$(date +%Y%m%d).json

# Мониторинг в реальном времени
watch -n 1 'docker-compose ps'
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи
2. Убедитесь в правильности токена
3. Проверьте права доступа к файлам
4. Убедитесь в доступности интернета
5. Проверьте версии Python и зависимостей
