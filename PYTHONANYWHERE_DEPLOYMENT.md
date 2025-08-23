# Развертывание на PythonAnywhere

Этот документ содержит пошаговые инструкции по размещению вашего приложения с рецептами на PythonAnywhere.

## Шаг 1: Регистрация на PythonAnywhere

1. Перейдите на [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Зарегистрируйтесь (бесплатный аккаунт)
3. Войдите в свой аккаунт

## Шаг 2: Создание нового веб-приложения

1. В панели управления PythonAnywhere найдите раздел "Web"
2. Нажмите "Add a new web app"
3. Выберите "Manual configuration"
4. Выберите Python версию 3.9 или выше
5. Запишите URL вашего приложения (например: `yourusername.pythonanywhere.com`)

## Шаг 3: Загрузка файлов

### Вариант 1: Через веб-интерфейс
1. Перейдите в раздел "Files"
2. Создайте папку для вашего проекта (например, `recipe_bot`)
3. Загрузите следующие файлы:
   - `web_app.py`
   - `pythonanywhere_config.py`
   - `requirements.txt`
   - `recipes.json`
   - Папку `templates` с файлом `index.html`

### Вариант 2: Через Git (рекомендуется)
1. В разделе "Consoles" откройте Bash консоль
2. Выполните команды:
```bash
cd ~
git clone https://github.com/yourusername/telegram_recipe_bot.git
cd telegram_recipe_bot
```

## Шаг 4: Установка зависимостей

1. В Bash консоли выполните:
```bash
pip install --user -r requirements.txt
```

## Шаг 5: Настройка веб-приложения

1. Перейдите в раздел "Web"
2. Нажмите на ваше веб-приложение
3. В разделе "Code" найдите "Source code" и укажите путь к папке с проектом
4. В разделе "WSGI configuration file" нажмите на файл конфигурации
5. Замените содержимое на:

```python
import sys
import os

# Добавляем путь к проекту
path = '/home/yourusername/recipe_bot'
if path not in sys.path:
    sys.path.append(path)

# Импортируем приложение
from web_app import app as application
```

**Важно:** Замените `yourusername` на ваше имя пользователя PythonAnywhere

## Шаг 6: Настройка переменных окружения

1. В разделе "Files" создайте файл `.env` в папке проекта
2. Добавьте необходимые переменные (если есть):
```
# Пример переменных окружения
DEBUG=False
```

## Шаг 7: Перезапуск приложения

1. В разделе "Web" нажмите кнопку "Reload" для вашего приложения
2. Дождитесь сообщения "Reloaded"

## Шаг 8: Проверка работы

1. Откройте URL вашего приложения в браузере
2. Убедитесь, что страница загружается и показывает интерфейс с рецептами
3. Проверьте работу кнопок и API

## Структура файлов на PythonAnywhere

```
/home/yourusername/recipe_bot/
├── web_app.py              # Основное Flask приложение
├── pythonanywhere_config.py # Конфигурация для PythonAnywhere
├── requirements.txt         # Зависимости Python
├── recipes.json            # Файл с рецептами
├── .env                    # Переменные окружения (если нужны)
└── templates/
    └── index.html          # HTML шаблон
```

## Возможные проблемы и решения

### Ошибка "Module not found"
- Убедитесь, что все зависимости установлены: `pip install --user -r requirements.txt`
- Проверьте правильность пути в WSGI файле

### Ошибка "Permission denied"
- Убедитесь, что файлы имеют правильные права доступа
- В Bash консоли выполните: `chmod 644 *.py *.html *.json`

### Приложение не загружается
- Проверьте логи в разделе "Web" → "Error log"
- Убедитесь, что WSGI файл правильно настроен
- Проверьте, что все импорты работают корректно

### Рецепты не отображаются
- Проверьте, что файл `recipes.json` загружен и имеет правильный формат
- Убедитесь, что файл доступен для чтения

## Обновление приложения

Для обновления приложения:
1. Загрузите новые файлы или выполните `git pull`
2. Перезапустите веб-приложение кнопкой "Reload"

## Мониторинг

В разделе "Web" вы можете:
- Просматривать логи ошибок
- Мониторить использование ресурсов
- Управлять настройками приложения

## Поддержка

Если возникли проблемы:
1. Проверьте логи ошибок
2. Обратитесь в [форум PythonAnywhere](https://www.pythonanywhere.com/forums/)
3. Создайте тикет в поддержке PythonAnywhere

## Полезные ссылки

- [Документация PythonAnywhere](https://help.pythonanywhere.com/)
- [Руководство по Flask на PythonAnywhere](https://help.pythonanywhere.com/pages/Flask/)
- [Форум PythonAnywhere](https://www.pythonanywhere.com/forums/)

