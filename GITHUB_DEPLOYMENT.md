# 🚀 Размещение проекта на GitHub и интеграция с сервером

## 📋 Обзор

Этот документ описывает полный процесс размещения вашего Telegram Recipe Bot на GitHub и настройки автоматического развертывания на сервер.

## 🎯 Что мы настроим

1. ✅ Git репозиторий
2. ✅ GitHub Actions для CI/CD
3. ✅ Автоматическое развертывание на сервер
4. ✅ Публикация Docker образов
5. ✅ Мониторинг и логирование

## 🚀 Быстрый старт

### 1. Запуск автоматической настройки

```bash
./setup-github.sh
```

### 2. Создание репозитория на GitHub

1. Перейдите на [github.com](https://github.com)
2. Нажмите "New repository"
3. Введите название: `telegram_recipe_bot`
4. Выберите "Public" или "Private"
5. НЕ создавайте README, .gitignore или license (у нас уже есть)
6. Нажмите "Create repository"

### 3. Подключение к GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/telegram_recipe_bot.git
git branch -M main
git push -u origin main
```

## 🔧 Настройка GitHub Actions

### 1. GitHub Secrets

Перейдите в настройки репозитория: `Settings` → `Secrets and variables` → `Actions`

Добавьте следующие секреты:

#### Для развертывания на сервер:
- `HOST` - IP адрес вашего сервера
- `USERNAME` - имя пользователя на сервере  
- `SSH_KEY` - приватный SSH ключ (содержимое файла `~/.ssh/id_rsa`)
- `PORT` - SSH порт (обычно 22)

#### Для Docker Hub (опционально):
- `DOCKER_USERNAME` - имя пользователя Docker Hub
- `DOCKER_PASSWORD` - пароль Docker Hub

### 2. Проверка Actions

После push в main ветку, GitHub Actions автоматически:
- Запустит тесты
- Развернет проект на сервер
- Опубликует Docker образ (если настроен)

## 🖥️ Настройка сервера

### 1. Предварительные требования

- Ubuntu/Debian сервер
- SSH доступ
- Docker и Docker Compose
- Git

### 2. Установка Docker

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагрузка
sudo reboot
```

### 3. Настройка SSH ключей

```bash
# На локальной машине
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Копирование на сервер
ssh-copy-id username@your_server_ip
```

### 4. Клонирование проекта

```bash
cd /home/username
git clone https://github.com/YOUR_USERNAME/telegram_recipe_bot.git
cd telegram_recipe_bot
```

### 5. Создание .env файла

```bash
cp env_example.txt .env
nano .env
```

Добавьте:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 6. Первый запуск

```bash
chmod +x deploy.sh
./deploy.sh
```

## 🔄 Рабочий процесс разработки

### 1. Внесение изменений

```bash
# Создание новой ветки
git checkout -b feature/new-feature

# Внесение изменений
# ...

# Коммит изменений
git add .
git commit -m "Add new feature"

# Push в GitHub
git push origin feature/new-feature
```

### 2. Создание Pull Request

1. Перейдите на GitHub
2. Нажмите "Compare & pull request"
3. Опишите изменения
4. Нажмите "Create pull request"

### 3. Автоматическое развертывание

После merge в main ветку:
- GitHub Actions автоматически запустится
- Код будет развернут на сервер
- Docker образ будет обновлен

## 📊 Мониторинг и логи

### 1. GitHub Actions

- Перейдите в `Actions` вкладку репозитория
- Просматривайте статус развертываний
- Проверяйте логи при ошибках

### 2. Сервер

```bash
# Статус Docker контейнеров
docker-compose ps

# Логи приложения
docker-compose logs -f

# Мониторинг ресурсов
docker stats
```

### 3. Telegram Bot

- Отправьте команду `/start` боту
- Проверьте ответы
- Просмотрите логи на сервере

## 🔧 Устранение неполадок

### Проблемы с GitHub Actions

1. **Проверьте Secrets** - все ли секреты добавлены правильно
2. **SSH подключение** - проверьте доступность сервера
3. **Права доступа** - убедитесь, что пользователь имеет права на сервере

### Проблемы с сервером

1. **Docker не запущен** - `sudo systemctl start docker`
2. **Права доступа** - `sudo chown -R $USER:$USER /path/to/project`
3. **Порт занят** - `sudo netstat -tulpn | grep :80`

### Проблемы с ботом

1. **Токен неверный** - проверьте .env файл
2. **Бот заблокирован** - проверьте статус в @BotFather
3. **Сеть недоступна** - проверьте интернет соединение

## 📈 Расширенные возможности

### 1. Автоматическое тестирование

Добавьте тесты в `tests/` папку:

```python
# tests/test_bot.py
import unittest
from bot import Bot

class TestBot(unittest.TestCase):
    def test_bot_initialization(self):
        bot = Bot()
        self.assertIsNotNone(bot)

if __name__ == '__main__':
    unittest.main()
```

### 2. Уведомления в Telegram

Настройте уведомления о развертывании:

```yaml
# В .github/workflows/deploy.yml добавьте:
- name: Notify deployment
  run: |
    curl -X POST "https://api.telegram.org/bot${{ secrets.BOT_TOKEN }}/sendMessage" \
      -d "chat_id=${{ secrets.CHAT_ID }}" \
      -d "text=🚀 Deployment completed successfully!"
```

### 3. Резервное копирование

Настройте автоматическое резервное копирование:

```bash
# backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz /path/to/project
aws s3 cp backup_$DATE.tar.gz s3://your-bucket/
```

## 🔐 Безопасность

### 1. Ограничение доступа

```bash
# Настройка файрвола
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Регулярные обновления

```bash
# Автоматические обновления
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Мониторинг безопасности

```bash
# Проверка подозрительной активности
sudo journalctl -f | grep "Failed password"
```

## 📚 Полезные ссылки

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [SSH Key Setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи GitHub Actions
2. Проверьте логи на сервере
3. Убедитесь в правильности настроек
4. Создайте Issue в репозитории

---

**Удачи с развертыванием! 🚀**
