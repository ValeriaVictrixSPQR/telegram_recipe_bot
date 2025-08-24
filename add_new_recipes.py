#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def add_new_recipes():
    # Читаем существующие рецепты
    with open('recipes.json', 'r', encoding='utf-8') as f:
        existing_recipes = json.load(f)
    
    # Читаем новые рецепты
    with open('/Users/valerii/Desktop/Рецепты 2.json', 'r', encoding='utf-8') as f:
        new_recipes = json.load(f)
    
    # Находим максимальный номер в существующих рецептах
    max_number = max(recipe['number'] for recipe in existing_recipes)
    print(f"Максимальный номер в существующих рецептах: {max_number}")
    
    # Добавляем новые рецепты, начиная с следующего номера
    for i, new_recipe in enumerate(new_recipes):
        # Создаем новый рецепт в нужном формате
        formatted_recipe = {
            "number": max_number + i + 1,
            "name": new_recipe["name"].upper(),
            "ingredients": new_recipe["ingredients"],
            "method": new_recipe["preparation"]
        }
        
        existing_recipes.append(formatted_recipe)
        print(f"Добавлен рецепт {formatted_recipe['number']}: {formatted_recipe['name']}")
    
    # Сохраняем обновленный файл
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(existing_recipes, f, ensure_ascii=False, indent=4)
    
    print(f"\nВсего добавлено {len(new_recipes)} новых рецептов")
    print(f"Общее количество рецептов: {len(existing_recipes)}")

if __name__ == "__main__":
    add_new_recipes()
