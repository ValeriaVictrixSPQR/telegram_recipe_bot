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
