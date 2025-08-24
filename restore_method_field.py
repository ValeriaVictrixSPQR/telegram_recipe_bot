#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def restore_method_field():
    """Восстанавливает поле method (инструкции по приготовлению) из резервной копии"""
    
    # Загружаем текущие рецепты (без поля method)
    with open('recipes.json', 'r', encoding='utf-8') as f:
        current_recipes = json.load(f)
    
    # Загружаем резервную копию с полным полем method
    with open('recipes_old_structure_backup.json', 'r', encoding='utf-8') as f:
        backup_recipes = json.load(f)
    
    print(f"Восстанавливаем поле 'method' для {len(current_recipes)} рецептов...")
    print("=" * 60)
    
    # Создаем словарь для быстрого поиска по номеру рецепта
    backup_dict = {recipe['number']: recipe for recipe in backup_recipes}
    
    # Восстанавливаем поле method
    restored_count = 0
    missing_method = 0
    
    for i, recipe in enumerate(current_recipes):
        recipe_number = recipe['number']
        
        if recipe_number in backup_dict:
            # Восстанавливаем поле method
            recipe['method'] = backup_dict[recipe_number].get('method', '')
            restored_count += 1
        else:
            # Если рецепт не найден в резервной копии
            recipe['method'] = 'Инструкция по приготовлению не указана'
            missing_method += 1
        
        # Показываем прогресс каждые 20 рецептов
        if (i + 1) % 20 == 0:
            print(f"Обработано: {i + 1}/{len(current_recipes)}")
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ ВОССТАНОВЛЕНИЯ:")
    print("=" * 60)
    
    print(f"Всего рецептов: {len(current_recipes)}")
    print(f"Восстановлено инструкций: {restored_count}")
    print(f"Без инструкций: {missing_method}")
    
    # Показываем примеры восстановленной структуры
    print("\nПримеры восстановленной структуры:")
    print("-" * 50)
    
    for i in range(min(3, len(current_recipes))):
        recipe = current_recipes[i]
        print(f"{i+1}. {recipe['name']}")
        print(f"   Номер: {recipe['number']}")
        print(f"   Время: {recipe['cooking_time']} минут")
        print(f"   Инструкция: {recipe['method'][:80]}...")
        print()
    
    # Сохраняем обновленные рецепты
    print(f"\nСохраняем обновленные рецепты...")
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(current_recipes, f, ensure_ascii=False, indent=4)
    
    print("✅ Готово! Файл recipes.json обновлен с полем 'method'.")
    
    # Создаем новую резервную копию
    new_backup = f'recipes_5_fields_backup.json'
    with open(new_backup, 'w', encoding='utf-8') as f:
        json.dump(current_recipes, f, ensure_ascii=False, indent=4)
    
    print(f"📁 Создана новая резервная копия: {new_backup}")
    
    # Показываем финальную структуру
    print(f"\n📋 Финальная структура рецепта:")
    print("-" * 30)
    print("1. number - порядковый номер")
    print("2. name - название рецепта")
    print("3. ingredients - ингредиенты")
    print("4. method - инструкция по приготовлению")
    print("5. cooking_time - время готовки")

if __name__ == "__main__":
    restore_method_field()
