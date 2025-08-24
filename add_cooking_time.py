#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

def extract_cooking_time(recipe):
    """Извлекает время готовки из рецепта (в минутах)"""
    method = recipe.get('method', '').lower()
    
    # Паттерны для поиска времени
    patterns = [
        r'(\d+)\s*минут',  # "25 минут"
        r'(\d+)\s*мин',    # "25 мин"
        r'(\d+)\s*м',      # "25 м"
        r'(\d+)\s*минуты', # "25 минуты"
        r'(\d+)\s*минуту', # "25 минуту"
        r'(\d+)\s*минут\b', # "25 минут" (с границей слова)
        r'(\d+)\s*мин\b',   # "25 мин" (с границей слова)
    ]
    
    max_time = 0
    found_times = []
    
    for pattern in patterns:
        matches = re.findall(pattern, method)
        for match in matches:
            time_value = int(match)
            found_times.append(time_value)
            if time_value > max_time:
                max_time = time_value
    
    return max_time, found_times

def analyze_and_update_recipes():
    """Анализирует рецепты и добавляет поле cooking_time"""
    
    # Загружаем рецепты
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
    
    print(f"Анализируем {len(recipes)} рецептов...")
    print("=" * 60)
    
    # Статистика
    total_recipes = len(recipes)
    recipes_with_time = 0
    recipes_without_time = 0
    time_distribution = {}
    
    # Обрабатываем каждый рецепт
    for i, recipe in enumerate(recipes):
        cooking_time, found_times = extract_cooking_time(recipe)
        
        # Добавляем поле cooking_time
        recipe['cooking_time'] = cooking_time
        
        # Статистика
        if cooking_time > 0:
            recipes_with_time += 1
            if cooking_time not in time_distribution:
                time_distribution[cooking_time] = 0
            time_distribution[cooking_time] += 1
        else:
            recipes_without_time += 1
        
        # Показываем прогресс каждые 20 рецептов
        if (i + 1) % 20 == 0:
            print(f"Обработано: {i + 1}/{total_recipes}")
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА:")
    print("=" * 60)
    
    print(f"Всего рецептов: {total_recipes}")
    print(f"С указанием времени: {recipes_with_time}")
    print(f"Без указания времени: {recipes_without_time}")
    print(f"Процент с временем: {(recipes_with_time/total_recipes)*100:.1f}%")
    
    print("\nРаспределение времени готовки:")
    print("-" * 40)
    
    # Сортируем по времени
    sorted_times = sorted(time_distribution.items())
    for time, count in sorted_times:
        print(f"{time:3d} минут: {count:3d} рецептов")
    
    # Анализ рецептов без времени
    if recipes_without_time > 0:
        print(f"\nРецепты без указания времени ({recipes_without_time}):")
        print("-" * 40)
        
        no_time_recipes = []
        for recipe in recipes:
            if recipe['cooking_time'] == 0:
                no_time_recipes.append(recipe['name'])
        
        # Показываем первые 10
        for i, name in enumerate(no_time_recipes[:10]):
            print(f"{i+1:2d}. {name}")
        
        if len(no_time_recipes) > 10:
            print(f"... и еще {len(no_time_recipes) - 10} рецептов")
    
    # Сохраняем обновленные рецепты
    print(f"\nСохраняем обновленные рецепты...")
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)
    
    print("✅ Готово! Файл recipes.json обновлен.")
    
    # Создаем резервную копию
    backup_filename = f'recipes_backup_{len(recipes)}_recipes.json'
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)
    
    print(f"📁 Создана резервная копия: {backup_filename}")

if __name__ == "__main__":
    analyze_and_update_recipes()
