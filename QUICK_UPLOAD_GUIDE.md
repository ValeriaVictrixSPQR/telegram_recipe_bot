# ⚡ Быстрая загрузка в PythonAnywhere

## 📦 Готовые файлы

Все необходимые файлы подготовлены и упакованы в архив:
- **`recipe_bot_pythonanywhere.zip`** (16.5 KB)

## 🚀 Быстрая загрузка

### 1. Загрузите архив
1. Войдите в [PythonAnywhere](https://www.pythonanywhere.com)
2. Перейдите в раздел "Files"
3. Создайте папку `recipe_bot`
4. Загрузите `recipe_bot_pythonanywhere.zip`
5. Распакуйте архив

### 2. Создайте веб-приложение
1. В разделе "Web" → "Add a new web app"
2. Выберите "Manual configuration"
3. Python 3.9+

### 3. Установите зависимости
```bash
pip install --user flask python-dotenv gunicorn
```

### 4. Настройте WSGI
В настройках веб-приложения:
- Укажите путь к `wsgi.py`
- Замените `yourusername` на ваше имя пользователя

### 5. Перезапустите
Нажмите "Reload" в разделе "Web"

## 📁 Структура файлов

```
recipe_bot/
├── web_app.py          # Flask приложение
├── wsgi.py             # WSGI конфигурация
├── requirements.txt    # Зависимости
├── recipes.json        # 90 рецептов
└── templates/
    └── index.html      # Веб-интерфейс
```

## ✅ Готово!

Откройте URL вашего приложения в браузере!

---
**Время загрузки: ~5 минут** ⏱️
