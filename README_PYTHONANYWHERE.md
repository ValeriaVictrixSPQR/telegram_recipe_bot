# 🚀 Быстрое развертывание на PythonAnywhere

## Что это?

Веб-версия бота с рецептами детского питания, адаптированная для размещения на PythonAnywhere.

## Быстрый старт

### 1. Зарегистрируйтесь на PythonAnywhere
- Перейдите на [pythonanywhere.com](https://www.pythonanywhere.com)
- Создайте бесплатный аккаунт

### 2. Создайте веб-приложение
- В разделе "Web" → "Add a new web app"
- Выберите "Manual configuration"
- Python 3.9+

### 3. Загрузите файлы
```
recipe_bot/
├── web_app.py          ← Основное приложение
├── wsgi.py             ← WSGI конфигурация
├── requirements.txt    ← Зависимости
├── recipes.json        ← Рецепты
└── templates/
    └── index.html      ← Веб-интерфейс
```

### 4. Установите зависимости
```bash
pip install --user -r requirements.txt
```

### 5. Настройте WSGI
В настройках веб-приложения укажите `wsgi.py` как WSGI файл.

### 6. Перезапустите
Нажмите "Reload" в разделе "Web".

## Структура проекта

- **`web_app.py`** - Flask приложение с API для рецептов
- **`wsgi.py`** - WSGI конфигурация для PythonAnywhere
- **`templates/index.html`** - Красивый веб-интерфейс
- **`recipes.json`** - База данных рецептов

## API эндпоинты

- `GET /` - Главная страница
- `GET /api/recipes` - Получить 3 случайных рецепта
- `GET /api/recipes/count` - Статистика рецептов
- `POST /api/recipes/reset` - Сбросить счетчик использованных

## Особенности

✅ Адаптировано для PythonAnywhere  
✅ Красивый веб-интерфейс  
✅ API для работы с рецептами  
✅ Отслеживание использованных рецептов  
✅ Адаптивный дизайн  

## Подробная инструкция

См. файл `PYTHONANYWHERE_DEPLOYMENT.md` для детального описания процесса развертывания.

## Поддержка

- [Документация PythonAnywhere](https://help.pythonanywhere.com/)
- [Форум PythonAnywhere](https://www.pythonanywhere.com/forums/)

