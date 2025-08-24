#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def restructure_recipes():
    """Изменяет структуру рецептов, оставляя только основные поля"""
    
    # Загружаем текущие рецепты
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
    
    print(f"Обрабатываем {len(recipes)} рецептов...")
    print("=" * 60)
    
    # Создаем новую структуру
    new_recipes = []
    
    for i, recipe in enumerate(recipes):
        # Создаем новый рецепт с нужными полями
        new_recipe = {
            "number": recipe.get('number', i + 1),
            "name": recipe.get('name', ''),
            "ingredients": recipe.get('ingredients', ''),
            "cooking_time": recipe.get('cooking_time', 0)
        }
        
        new_recipes.append(new_recipe)
        
        # Показываем прогресс каждые 20 рецептов
        if (i + 1) % 20 == 0:
            print(f"Обработано: {i + 1}/{len(recipes)}")
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ ПРЕОБРАЗОВАНИЯ:")
    print("=" * 60)
    
    print(f"Всего рецептов: {len(new_recipes)}")
    
    # Показываем примеры новой структуры
    print("\nПримеры новой структуры:")
    print("-" * 40)
    
    for i in range(min(5, len(new_recipes))):
        recipe = new_recipes[i]
        print(f"{i+1}. {recipe['name']}")
        print(f"   Номер: {recipe['number']}")
        print(f"   Время: {recipe['cooking_time']} минут")
        print(f"   Ингредиенты: {recipe['ingredients'][:50]}...")
        print()
    
    # Создаем резервную копию текущего файла
    backup_filename = 'recipes_old_structure_backup.json'
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)
    
    print(f"📁 Создана резервная копия старой структуры: {backup_filename}")
    
    # Сохраняем новую структуру
    print(f"\nСохраняем новую структуру...")
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(new_recipes, f, ensure_ascii=False, indent=4)
    
    print("✅ Готово! Файл recipes.json обновлен с новой структурой.")
    
    # Статистика по времени готовки
    time_stats = {}
    for recipe in new_recipes:
        time = recipe['cooking_time']
        if time not in time_stats:
            time_stats[time] = 0
        time_stats[time] += 1
    
    print(f"\n📊 Статистика времени готовки:")
    print("-" * 30)
    
    # Сортируем по времени
    sorted_times = sorted(time_stats.items())
    for time, count in sorted_times:
        if time == 0:
            print(f"Без указания времени: {count} рецептов")
        else:
            print(f"{time:3d} минут: {count:3d} рецептов")

if __name__ == "__main__":
    restructure_recipes()
