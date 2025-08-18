# 🚀 Интеграция с AMVERA через GitHub

## 📋 Обзор

Этот документ описывает, как настроить автоматическое развертывание вашего Telegram Recipe Bot на платформе AMVERA через GitHub Actions.

## 🎯 Что мы настроим

1. ✅ Веб-версию приложения для AMVERA
2. ✅ GitHub Actions для автоматического развертывания
3. ✅ Интеграцию с AMVERA через SSH
4. ✅ Мониторинг и логирование

## 🔧 Подготовка проекта

### 1. Структура файлов

Убедитесь, что у вас есть следующие файлы:
- `web_app.py` - веб-версия приложения
- `amvera.yaml` - конфигурация для AMVERA
- `Dockerfile` - для сборки Docker образа
- `requirements.txt` - зависимости Python
- `.github/workflows/amvera-deploy.yml` - GitHub Actions

### 2. Проверка конфигурации

#### amvera.yaml
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: telegram-recipe-web
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - PORT=8000
    volumes:
      - ./recipes.json:/app/recipes.json:ro
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    networks:
      - web-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  web-network:
    driver: bridge

volumes:
  logs:
```

## 🖥️ Настройка AMVERA

### 1. Создание проекта на AMVERA

1. Перейдите на [cloud.amvera.ru](https://cloud.amvera.ru)
2. Войдите в свой аккаунт
3. Создайте новый проект с названием `telegram-recipe-bot`
4. Выберите тип "Docker"

### 2. Настройка Git репозитория

В разделе "Репозиторий":
1. Подключите ваш GitHub репозиторий
2. Укажите ветку `main` или `master`
3. Настройте автоматическое развертывание

### 3. Настройка переменных окружения

В разделе "Переменные":
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота

### 4. Настройка доменов

В разделе "Домены":
- Подключите бесплатный домен AMVERA
- Или настройте свой домен

## 🔑 Настройка GitHub Secrets

### 1. Перейдите в настройки репозитория

`Settings` → `Secrets and variables` → `Actions`

### 2. Добавьте следующие секреты:

#### Основные секреты для AMVERA:
- `AMVERA_HOST` - IP адрес вашего AMVERA сервера
- `AMVERA_USERNAME` - имя пользователя на AMVERA
- `AMVERA_SSH_KEY` - приватный SSH ключ
- `AMVERA_PORT` - SSH порт (обычно 22)

#### Секреты для бота:
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота

### 3. Получение SSH ключа

```bash
# Генерация SSH ключа (если нет)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Копирование публичного ключа на AMVERA
ssh-copy-id username@amvera_server_ip

# Проверка подключения
ssh username@amvera_server_ip
```

## 🚀 Первое развертывание

### 1. Запуск GitHub Actions

После настройки секретов:
1. Сделайте push в main ветку
2. GitHub Actions автоматически запустится
3. Проверьте статус в разделе Actions

### 2. Проверка развертывания

```bash
# Подключение к AMVERA серверу
ssh username@amvera_server_ip

# Проверка статуса контейнеров
docker-compose ps

# Просмотр логов
docker-compose logs -f

# Проверка здоровья приложения
curl http://localhost:8000/health
```

### 3. Проверка веб-интерфейса

Откройте ваш домен AMVERA в браузере:
- Должна загрузиться страница с рецептами
- Кнопка "Получить 3 случайных рецепта" должна работать
- API эндпоинты должны отвечать

## 📊 API эндпоинты

### Доступные эндпоинты:

- `/` - главная страница с веб-интерфейсом
- `/health` - проверка здоровья приложения
- `/api/stats` - статистика (количество рецептов)
- `/api/random-recipes` - 3 случайных рецепта
- `/api/recipes` - все рецепты

### Тестирование API:

```bash
# Проверка здоровья
curl http://your-domain.amvera.run/health

# Получение статистики
curl http://your-domain.amvera.run/api/stats

# Получение случайных рецептов
curl http://your-domain.amvera.run/api/random-recipes
```

## 🔄 Рабочий процесс разработки

### 1. Внесение изменений

```bash
# Создание новой ветки
git checkout -b feature/new-feature

# Внесение изменений
# ...

# Коммит и push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

### 2. Создание Pull Request

1. Перейдите на GitHub
2. Создайте Pull Request
3. Опишите изменения
4. Дождитесь проверок

### 3. Автоматическое развертывание

После merge в main ветку:
- GitHub Actions автоматически запустится
- Код будет развернут на AMVERA
- Приложение будет перезапущено

## 📈 Мониторинг и логи

### 1. GitHub Actions

- Перейдите в `Actions` вкладку репозитория
- Просматривайте статус развертываний
- Проверяйте логи при ошибках

### 2. AMVERA

```bash
# Статус контейнеров
docker-compose ps

# Логи приложения
docker-compose logs -f web

# Мониторинг ресурсов
docker stats

# Проверка портов
netstat -tulpn | grep :8000
```

### 3. Веб-интерфейс

- Откройте ваш домен в браузере
- Проверьте работу кнопок
- Просмотрите консоль браузера на ошибки

## 🔧 Устранение неполадок

### Проблемы с GitHub Actions

1. **Проверьте Secrets** - все ли секреты добавлены правильно
2. **SSH подключение** - проверьте доступность AMVERA сервера
3. **Права доступа** - убедитесь, что пользователь имеет права

### Проблемы с AMVERA

1. **Docker не запущен** - `sudo systemctl start docker`
2. **Права доступа** - `sudo chown -R $USER:$USER /path/to/project`
3. **Порт занят** - `sudo netstat -tulpn | grep :8000`

### Проблемы с веб-приложением

1. **Приложение не запускается** - проверьте логи Docker
2. **Ошибки 500** - проверьте синтаксис Python кода
3. **Статические файлы не загружаются** - проверьте пути в коде

## 📝 Полезные команды

### Docker команды:
```bash
# Перезапуск сервиса
docker-compose restart web

# Остановка сервиса
docker-compose down

# Просмотр использования ресурсов
docker stats

# Очистка неиспользуемых образов
docker system prune -a
```

### Системные команды:
```bash
# Проверка места на диске
df -h

# Проверка использования памяти
free -h

# Проверка активных процессов
ps aux | grep python
```

## 🔐 Безопасность

### 1. Ограничение доступа

```bash
# Настройка файрвола
sudo ufw allow ssh
sudo ufw allow 8000
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

# Проверка открытых портов
sudo netstat -tulpn
```

## 📚 Полезные ссылки

- [AMVERA Documentation](https://docs.amvera.ru/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи GitHub Actions
2. Проверьте логи на AMVERA сервере
3. Убедитесь в правильности настроек
4. Создайте Issue в репозитории
5. Обратитесь в поддержку AMVERA

---

**Удачи с развертыванием на AMVERA! 🚀**
