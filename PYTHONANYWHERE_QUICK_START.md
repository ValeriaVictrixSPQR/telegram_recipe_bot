# 🚀 Быстрое развертывание на PythonAnywhere

## Шаг 1: Регистрация
1. Перейдите на [pythonanywhere.com](https://www.pythonanywhere.com)
2. Создайте бесплатный аккаунт
3. Войдите в панель управления

## Шаг 2: Создание веб-приложения
1. В разделе "Web" → "Add a new web app"
2. Выберите "Manual configuration"
3. Python 3.9 или выше
4. Запишите URL (например: `yourusername.pythonanywhere.com`)

## Шаг 3: Загрузка файлов
### Через Git (рекомендуется):
```bash
cd ~
git clone https://github.com/yourusername/telegram_recipe_bot.git
cd telegram_recipe_bot
```

### Или через веб-интерфейс:
Загрузите эти файлы в папку проекта:
- `web_app.py`
- `wsgi.py`
- `requirements.txt`
- `recipes.json`
- Папку `templates/` с `index.html`

## Шаг 4: Установка зависимостей
```bash
pip install --user -r requirements.txt
```

## Шаг 5: Настройка WSGI
1. В разделе "Web" → ваше приложение
2. Нажмите на WSGI файл
3. Замените содержимое на:

```python
import sys
import os

# Добавляем путь к проекту
path = '/home/yourusername/telegram_recipe_bot'
if path not in sys.path:
    sys.path.append(path)

# Импортируем приложение
from web_app import app as application
```

**Важно:** Замените `yourusername` на ваше имя пользователя!

## Шаг 6: Перезапуск
1. Нажмите "Reload" в разделе "Web"
2. Дождитесь сообщения "Reloaded"

## Шаг 7: Проверка
Откройте URL вашего приложения в браузере!

## Структура файлов
```
/home/yourusername/telegram_recipe_bot/
├── web_app.py          # Flask приложение
├── wsgi.py             # WSGI конфигурация
├── requirements.txt    # Зависимости
├── recipes.json        # База рецептов
└── templates/
    └── index.html      # Веб-интерфейс
```

## Возможные проблемы

### "Module not found"
```bash
pip install --user flask python-dotenv
```

### "Permission denied"
```bash
chmod 644 *.py *.html *.json
```

### Приложение не загружается
- Проверьте логи в "Web" → "Error log"
- Убедитесь, что путь в WSGI файле правильный

## API эндпоинты
- `GET /` - Главная страница
- `GET /api/recipes` - 3 случайных рецепта
- `GET /api/recipes/count` - Статистика
- `POST /api/recipes/reset` - Сброс счетчика

## Поддержка
- [Документация PythonAnywhere](https://help.pythonanywhere.com/)
- [Форум PythonAnywhere](https://www.pythonanywhere.com/forums/)

---
**Готово!** Ваше приложение с рецептами теперь доступно онлайн! 🎉
