# 📤 Загрузка файлов в PythonAnywhere

## 🎯 Способ 1: Загрузка архива (рекомендуется)

### 1. Скачайте архив
Файл `recipe_bot_pythonanywhere.zip` содержит все необходимые файлы.

### 2. Загрузите в PythonAnywhere
1. Войдите в аккаунт PythonAnywhere
2. Перейдите в раздел "Files"
3. Создайте папку для проекта (например, `recipe_bot`)
4. Перейдите в созданную папку
5. Нажмите "Upload a file" и выберите `recipe_bot_pythonanywhere.zip`
6. После загрузки нажмите на архив правой кнопкой мыши
7. Выберите "Extract here"

## 🎯 Способ 2: Загрузка отдельных файлов

### Необходимые файлы:
```
recipe_bot/
├── web_app.py          # Flask приложение
├── wsgi.py             # WSGI конфигурация
├── requirements.txt    # Зависимости
├── recipes.json        # База рецептов
└── templates/
    └── index.html      # Веб-интерфейс
```

### Пошаговая загрузка:

1. **Создайте папку проекта**
   - В разделе "Files" создайте папку `recipe_bot`

2. **Создайте папку templates**
   - В папке `recipe_bot` создайте подпапку `templates`

3. **Загрузите файлы по одному:**
   - `web_app.py` → в папку `recipe_bot`
   - `wsgi.py` → в папку `recipe_bot`
   - `requirements.txt` → в папку `recipe_bot`
   - `recipes.json` → в папку `recipe_bot`
   - `index.html` → в папку `recipe_bot/templates`

## 🎯 Способ 3: Копирование содержимого

### Для каждого файла:
1. Откройте файл в текстовом редакторе
2. Скопируйте содержимое
3. В PythonAnywhere создайте новый файл с тем же именем
4. Вставьте содержимое

## 📋 Содержимое файлов

### web_app.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import random
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)

# Загружаем рецепты из файла
def load_recipes():
    try:
        with open('recipes.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Проверяем, является ли data списком (прямая структура) или словарем с ключом 'recipes'
            if isinstance(data, list):
                return {"recipes": data}
            elif 'recipes' in data and isinstance(data['recipes'], list):
                return data
            else:
                print("Ошибка: Неверная структура файла recipes.json")
                return {"recipes": []}
    except FileNotFoundError:
        print("Файл recipes.json не найден. Создайте файл с рецептами.")
        return {"recipes": []}
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON файла: {e}")
        return {"recipes": []}
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке рецептов: {e}")
        return {"recipes": []}

# Глобальная переменная для хранения рецептов
RECIPES = load_recipes()
USED_RECIPE_IDS = set()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/recipes')
def get_recipes():
    """API для получения трех случайных рецептов"""
    try:
        if not RECIPES["recipes"]:
            return jsonify({"error": "Рецепты не найдены"}), 404
        
        # Получаем доступные рецепты
        available_recipes = [r for r in RECIPES["recipes"] if r["number"] not in USED_RECIPE_IDS]
        
        # Если все рецепты были показаны, сбрасываем счетчик
        if len(available_recipes) < 3:
            USED_RECIPE_IDS.clear()
            available_recipes = RECIPES["recipes"]
        
        # Проверяем, что у нас достаточно рецептов
        if len(available_recipes) < 3:
            return jsonify({"error": "Недостаточно рецептов для показа. Нужно минимум 3 рецепта."}), 400
        
        # Выбираем три случайных рецепта
        selected_recipes = random.sample(available_recipes, 3)
        
        # Добавляем номер выбранных рецептов в использованные
        for recipe in selected_recipes:
            USED_RECIPE_IDS.add(recipe["number"])
        
        return jsonify({
            "success": True,
            "recipes": selected_recipes,
            "total_recipes": len(RECIPES["recipes"])
        })
        
    except Exception as e:
        return jsonify({"error": f"Ошибка сервера: {str(e)}"}), 500

@app.route('/api/recipes/count')
def get_recipe_count():
    """API для получения количества рецептов"""
    return jsonify({
        "total_recipes": len(RECIPES["recipes"]),
        "used_recipes": len(USED_RECIPE_IDS)
    })

@app.route('/api/recipes/reset')
def reset_used_recipes():
    """API для сброса счетчика использованных рецептов"""
    global USED_RECIPE_IDS
    USED_RECIPE_IDS.clear()
    return jsonify({"success": True, "message": "Счетчик использованных рецептов сброшен"})

if __name__ == '__main__':
    # Для локальной разработки
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Для PythonAnywhere
    app = app
```

### wsgi.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WSGI файл для PythonAnywhere
Этот файл должен быть указан в настройках веб-приложения PythonAnywhere
"""

import sys
import os

# Добавляем путь к проекту в sys.path
# Замените 'yourusername' на ваше имя пользователя PythonAnywhere
project_path = '/home/yourusername/recipe_bot'
if project_path not in sys.path:
    sys.path.append(project_path)

# Импортируем Flask приложение
from web_app import app as application

# Для отладки (можно убрать в продакшене)
if __name__ == '__main__':
    application.run()
```

### requirements.txt
```
flask>=2.3.0
python-dotenv==1.0.0
gunicorn>=21.0.0
```

### templates/index.html
[Содержимое файла index.html - см. файл templates/index.html]

## 🔧 После загрузки файлов

1. **Установите зависимости:**
   ```bash
   pip install --user -r requirements.txt
   ```

2. **Настройте WSGI файл:**
   - В разделе "Web" → ваше приложение
   - Нажмите на WSGI файл
   - Замените `yourusername` на ваше имя пользователя

3. **Перезапустите приложение:**
   - Нажмите "Reload" в разделе "Web"

## ✅ Проверка

После загрузки и настройки откройте URL вашего приложения в браузере!

---
**Успешной загрузки!** 🚀
