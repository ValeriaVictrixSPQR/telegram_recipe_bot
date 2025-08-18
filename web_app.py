#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import random
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)

# HTML шаблон для веб-интерфейса
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍽️ Рецепты детского питания</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .recipe-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .recipe-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #fff;
        }
        .recipe-section {
            margin: 10px 0;
        }
        .recipe-section strong {
            color: #ffd700;
        }
        .btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            transition: transform 0.3s ease;
            display: block;
            margin: 20px auto;
            text-decoration: none;
            text-align: center;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        .stats {
            text-align: center;
            margin: 20px 0;
            font-size: 1.1em;
            color: #ffd700;
        }
        .loading {
            text-align: center;
            font-size: 1.2em;
            margin: 20px 0;
        }
        .error {
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid rgba(255, 0, 0, 0.5);
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍽️ Рецепты детского питания</h1>
        
        <div class="stats">
            📚 Всего рецептов: <span id="total-recipes">0</span>
        </div>
        
        <button class="btn" onclick="getRandomRecipes()">🎲 Получить 3 случайных рецепта</button>
        
        <div id="recipes-container">
            <div class="loading">Нажмите кнопку, чтобы получить рецепты!</div>
        </div>
    </div>

    <script>
        let usedRecipes = new Set();
        
        async function getRandomRecipes() {
            const container = document.getElementById('recipes-container');
            container.innerHTML = '<div class="loading">Загружаем рецепты...</div>';
            
            try {
                const response = await fetch('/api/random-recipes');
                const data = await response.json();
                
                if (data.success) {
                    displayRecipes(data.recipes);
                    updateStats();
                } else {
                    container.innerHTML = `<div class="error">❌ ${data.message}</div>`;
                }
            } catch (error) {
                container.innerHTML = `<div class="error">❌ Ошибка загрузки: ${error.message}</div>`;
            }
        }
        
        function displayRecipes(recipes) {
            const container = document.getElementById('recipes-container');
            let html = '';
            
            recipes.forEach((recipe, index) => {
                html += `
                    <div class="recipe-card">
                        <div class="recipe-title">${index + 1}. ${recipe.name}</div>
                        <div class="recipe-section">
                            <strong>🥘 Ингредиенты:</strong> ${recipe.ingredients}
                        </div>
                        <div class="recipe-section">
                            <strong>📝 Приготовление:</strong> ${recipe.instructions}
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        }
        
        function updateStats() {
            const totalElement = document.getElementById('total-recipes');
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        totalElement.textContent = data.total_recipes;
                    }
                });
        }
        
        // Загружаем статистику при загрузке страницы
        updateStats();
    </script>
</body>
</html>
"""

# Загружаем рецепты из файла
def load_recipes():
    try:
        with open('recipes.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'recipes' in data and isinstance(data['recipes'], list):
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Эндпоинт для проверки здоровья приложения"""
    return jsonify({"status": "healthy", "message": "Приложение работает"})

@app.route('/api/stats')
def stats():
    """API для получения статистики"""
    return jsonify({
        "success": True,
        "total_recipes": len(RECIPES["recipes"])
    })

@app.route('/api/random-recipes')
def random_recipes():
    """API для получения случайных рецептов"""
    if not RECIPES["recipes"]:
        return jsonify({
            "success": False,
            "message": "Рецепты не найдены. Проверьте файл recipes.json"
        })
    
    available_recipes = [r for r in RECIPES["recipes"] if r["id"] not in USED_RECIPE_IDS]
    
    if len(available_recipes) < 3:
        USED_RECIPE_IDS.clear()
        available_recipes = RECIPES["recipes"]
    
    if len(available_recipes) < 3:
        return jsonify({
            "success": False,
            "message": "Недостаточно рецептов для показа. Нужно минимум 3 рецепта."
        })
    
    selected_recipes = random.sample(available_recipes, 3)
    
    for recipe in selected_recipes:
        USED_RECIPE_IDS.add(recipe["id"])
    
    return jsonify({
        "success": True,
        "recipes": selected_recipes
    })

@app.route('/api/recipes')
def all_recipes():
    """API для получения всех рецептов"""
    return jsonify({
        "success": True,
        "recipes": RECIPES["recipes"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Загружено {len(RECIPES['recipes'])} рецептов")
    print(f"Веб-приложение запущено на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
