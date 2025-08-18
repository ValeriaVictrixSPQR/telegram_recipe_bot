# 🚀 Быстрое развертывание на сервере

## ⚡ 5 минут до запуска бота

### 1. Подготовка сервера (Ubuntu/Debian)

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Перезагружаемся или перелогиниваемся
sudo reboot
```

### 2. Клонирование и настройка

```bash
# Клонируем проект
git clone <your-repo-url>
cd telegram_recipe_bot

# Создаем .env файл
echo "TELEGRAM_BOT_TOKEN=YOUR_ACTUAL_TOKEN" > .env

# Делаем скрипты исполняемыми
chmod +x deploy.sh
```

### 3. Запуск

```bash
# Автоматическое развертывание
./deploy.sh
```

### 4. Проверка

```bash
# Статус контейнеров
docker-compose ps

# Логи
docker-compose logs -f
```

## 🔧 Альтернативный способ (без Docker)

```bash
# Простое развертывание
chmod +x deploy_simple.sh
./deploy_simple.sh

# Запуск
source venv/bin/activate
python3 bot.py
```

## 📊 Мониторинг

```bash
# Запуск мониторинга
./monitor.sh
```

## 🛑 Остановка

```bash
# Docker
docker-compose down

# Простой способ
# Ctrl+C в терминале
```

## 🚨 Если что-то пошло не так

1. Проверьте логи: `docker-compose logs`
2. Убедитесь в правильности токена в `.env`
3. Проверьте права доступа: `ls -la`
4. Перезапустите: `docker-compose restart`

## 📞 Быстрая помощь

```bash
# Перезапуск всего
docker-compose down && docker-compose up --build -d

# Очистка и пересборка
docker system prune -a && docker-compose up --build -d
```

**Готово! Ваш бот работает на сервере! 🎉**


