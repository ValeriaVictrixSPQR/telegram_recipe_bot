# 🖥️ Настройка сервера для интеграции с GitHub

## 📋 Предварительные требования

- Ubuntu/Debian сервер с SSH доступом
- Docker и Docker Compose установлены
- Git установлен
- SSH ключи настроены

## 🔑 Настройка SSH ключей

### 1. Генерация SSH ключа на локальной машине

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

### 2. Копирование публичного ключа на сервер

```bash
ssh-copy-id username@your_server_ip
```

### 3. Проверка подключения

```bash
ssh username@your_server_ip
```

## 🐳 Установка Docker

### Ubuntu/Debian

```bash
# Обновление пакетов
sudo apt update

# Установка зависимостей
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Добавление GPG ключа Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Добавление репозитория Docker
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Установка Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагрузка для применения изменений
sudo reboot
```

## 📁 Настройка проекта на сервере

### 1. Клонирование репозитория

```bash
cd /home/username
git clone https://github.com/your_username/telegram_recipe_bot.git
cd telegram_recipe_bot
```

### 2. Создание .env файла

```bash
cp env_example.txt .env
nano .env
```

Добавьте ваш токен бота:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 3. Настройка прав доступа

```bash
chmod +x deploy.sh
chmod +x deploy_simple.sh
chmod +x monitor.sh
```

## 🔄 Настройка автоматического развертывания

### 1. Создание скрипта для обновления

```bash
nano update.sh
```

Содержимое:
```bash
#!/bin/bash
cd /home/username/telegram_recipe_bot
git pull origin main
docker-compose down
docker-compose up --build -d
echo "Update completed at $(date)"
```

### 2. Настройка прав доступа

```bash
chmod +x update.sh
```

### 3. Тестирование развертывания

```bash
./deploy.sh
```

## 🚀 Запуск проекта

### Первый запуск

```bash
cd /home/username/telegram_recipe_bot
docker-compose up --build -d
```

### Проверка статуса

```bash
docker-compose ps
docker-compose logs -f
```

## 📊 Мониторинг

### Запуск мониторинга

```bash
./monitor.sh
```

### Проверка логов

```bash
# Docker логи
docker-compose logs -f

# Системные логи
sudo journalctl -u telegram-bot -f
```

## 🔧 Устранение неполадок

### Проблемы с правами доступа

```bash
sudo chown -R $USER:$USER /home/username/telegram_recipe_bot
```

### Проблемы с Docker

```bash
# Перезапуск Docker
sudo systemctl restart docker

# Проверка статуса
sudo systemctl status docker
```

### Проблемы с Git

```bash
# Проверка подключения к GitHub
ssh -T git@github.com

# Настройка Git
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

## 🔐 Безопасность

### 1. Настройка файрвола

```bash
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Регулярные обновления

```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Мониторинг безопасности

```bash
# Проверка открытых портов
sudo netstat -tulpn

# Проверка активных соединений
sudo ss -tulpn
```

## 📝 Полезные команды

```bash
# Перезапуск сервиса
docker-compose restart

# Остановка сервиса
docker-compose down

# Просмотр использования ресурсов
docker stats

# Очистка неиспользуемых образов
docker system prune -a

# Проверка места на диске
df -h

# Проверка использования памяти
free -h
```
