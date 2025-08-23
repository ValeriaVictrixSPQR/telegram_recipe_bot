# 🚂 Развертывание Telegram бота на Railway

## 🎯 Что такое Railway?

[Railway](https://railway.com) - это современная платформа для развертывания приложений, которая упрощает процесс деплоя и масштабирования. Идеально подходит для Telegram ботов!

## ✨ Преимущества Railway для Telegram ботов

- ✅ **Бесплатный план** - 500 часов в месяц
- ✅ **Автоматический деплой** из GitHub
- ✅ **Переменные окружения** - безопасное хранение токенов
- ✅ **Мониторинг** и логи в реальном времени
- ✅ **Простота настройки** - минимум конфигурации
- ✅ **Поддержка Docker** - автоматическое определение

## 🚀 Быстрый старт

### 1. Подготовка репозитория

Убедитесь, что в вашем GitHub репозитории есть:
- `bot.py` - основной файл бота
- `requirements.txt` - зависимости Python
- `recipes.json` - база рецептов
- `Dockerfile` - конфигурация Docker (опционально)

### 2. Регистрация на Railway

1. Перейдите на [railway.com](https://railway.com)
2. Нажмите "Start a New Project"
3. Выберите "Deploy from GitHub repo"
4. Подключите ваш GitHub аккаунт
5. Выберите репозиторий с ботом

### 3. Настройка переменных окружения

1. В проекте Railway перейдите в раздел "Variables"
2. Добавьте переменную:
   - **Ключ:** `8424689402:AAEWrilYr8sz1JVM6zSvaY3akg0nG029RcM`
   - **Значение:** ваш токен Telegram бота

### 4. Настройка деплоя

1. Railway автоматически определит, что это Python проект
2. Если есть Dockerfile, он будет использован
3. Если нет Dockerfile, Railway создаст его автоматически

### 5. Запуск

1. Нажмите "Deploy Now"
2. Дождитесь завершения сборки
3. Бот автоматически запустится

## 📋 Структура файлов

```
telegram_recipe_bot/
├── bot.py              # Основной файл бота
├── requirements.txt    # Зависимости Python
├── recipes.json        # База рецептов
├── Dockerfile          # Конфигурация Docker
├── .dockerignore       # Исключения для Docker
└── templates/          # Шаблоны (если нужны)
    └── index.html
```

## 🔧 Конфигурация

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY recipes.json .
COPY templates/ ./templates/

RUN useradd -m -u 1000 webuser && chown -R webuser:webuser /app
USER webuser

EXPOSE 8000

RUN python3 -c "import telegram; print('Telegram library imported successfully')"

CMD ["python3", "bot.py"]
```

### requirements.txt
```
python-telegram-bot>=22.3
python-dotenv==1.0.0
```

## 🌐 Переменные окружения

### Обязательные
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота

### Опциональные
- `DEBUG` - режим отладки (true/false)
- `LOG_LEVEL` - уровень логирования

## 📊 Мониторинг

### Логи
- В Railway Dashboard → ваш проект → "Deployments"
- Нажмите на последний деплой → "View Logs"

### Метрики
- Railway автоматически показывает использование ресурсов
- Мониторинг в реальном времени

## 🔄 Обновления

### Автоматические
- При push в main/master ветку
- Railway автоматически пересоберет и перезапустит бота

### Ручные
- В Railway Dashboard → "Deployments" → "Deploy Now"

## 🐛 Устранение неполадок

### Бот не запускается
1. Проверьте логи в Railway Dashboard
2. Убедитесь, что токен установлен правильно
3. Проверьте, что все файлы загружены

### Ошибки сборки
1. Проверьте `requirements.txt`
2. Убедитесь в корректности `Dockerfile`
3. Проверьте логи сборки

### Бот не отвечает
1. Проверьте, что бот запущен (логи)
2. Убедитесь, что токен действителен
3. Проверьте права бота в Telegram

## 💰 Стоимость

### Бесплатный план
- 500 часов в месяц
- 512 MB RAM
- 1 GB дискового пространства
- Подходит для большинства ботов

### Платные планы
- От $5/месяц
- Больше ресурсов
- Приоритетная поддержка

## 🔗 Полезные ссылки

- [Документация Railway](https://docs.railway.app/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)

## ✅ Готово!

После выполнения всех шагов ваш Telegram бот будет работать на Railway!

---
**Удачного развертывания!** 🚂
