# 🚀 Быстрое развертывание на AMVERA

## ⚡ Экспресс-настройка за 5 минут

### 1. Подготовка проекта
```bash
# Запуск автоматической настройки
./setup-github.sh

# Добавление всех файлов
git add .
git commit -m "Setup for AMVERA deployment"
```

### 2. Создание репозитория на GitHub
1. Создайте новый репозиторий `telegram_recipe_bot`
2. НЕ создавайте README, .gitignore или license
3. Скопируйте URL репозитория

### 3. Подключение к GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/telegram_recipe_bot.git
git branch -M main
git push -u origin main
```

### 4. Настройка GitHub Secrets
В `Settings` → `Secrets and variables` → `Actions` добавьте:

**Обязательные:**
- `AMVERA_HOST` - IP вашего AMVERA сервера
- `AMVERA_USERNAME` - имя пользователя на AMVERA
- `AMVERA_SSH_KEY` - приватный SSH ключ
- `AMVERA_PORT` - SSH порт (22)
- `TELEGRAM_BOT_TOKEN` - токен вашего бота

### 5. Настройка AMVERA
1. Создайте проект на [cloud.amvera.ru](https://cloud.amvera.ru)
2. Выберите тип "Docker"
3. Подключите GitHub репозиторий
4. Добавьте переменную `TELEGRAM_BOT_TOKEN`

### 6. Автоматическое развертывание
После push в main ветку:
- GitHub Actions автоматически запустится
- Код будет развернут на AMVERA
- Приложение будет доступно по вашему домену

## 🔍 Проверка работы

### Веб-интерфейс:
- Откройте ваш домен AMVERA
- Должна загрузиться страница с рецептами
- Кнопка "Получить 3 случайных рецепта" работает

### API эндпоинты:
```bash
# Проверка здоровья
curl http://your-domain.amvera.run/health

# Получение рецептов
curl http://your-domain.amvera.run/api/random-recipes
```

## 🆘 Если что-то не работает

1. **Проверьте GitHub Actions** - статус в разделе Actions
2. **Проверьте логи AMVERA** - `docker-compose logs -f`
3. **Проверьте переменные** - все ли секреты добавлены
4. **Проверьте SSH доступ** - `ssh username@amvera_ip`

## 📚 Подробная документация

- [AMVERA_SETUP.md](AMVERA_SETUP.md) - Полная инструкция по AMVERA
- [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) - Детали GitHub интеграции

---

**Готово! Ваш бот теперь работает на AMVERA! 🎉**
