import os
import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

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

# Глобальные переменные
RECIPES = load_recipes()
USED_RECIPE_IDS = set()

# Хранилище пользовательских данных (в реальном проекте лучше использовать базу данных)
USER_DATA = {}

def get_user_data(user_id):
    """Получает данные пользователя"""
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {
            'favorites': [],
            'preferences': {
                'allergies': [],
                'cooking_time': None
            }
        }
    return USER_DATA[user_id]

def save_user_data(user_id, data):
    """Сохраняет данные пользователя"""
    USER_DATA[user_id] = data

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start - главное меню"""
    keyboard = [
        [InlineKeyboardButton("📋 Получить рецепт", callback_data="show_recipes")],
        [InlineKeyboardButton("⭐ Избранное", callback_data="show_favorites")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="show_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Привет! Я бот с рецептами для детей.\n\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает настройки пользователя"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    prefs = user_data['preferences']
    
    # Формируем текст с текущими настройками
    settings_text = "⚙️ <b>Настройки</b>\n\n"
    
    # Аллергии
    allergies_text = ", ".join(prefs['allergies']) if prefs['allergies'] else "не указаны"
    settings_text += f"⚠️ Аллергии: {allergies_text}\n"
    
    # Время готовки
    time_text = prefs['cooking_time'] if prefs['cooking_time'] else "не указано"
    settings_text += f"⏰ Время готовки: {time_text}\n"
    
    # Кнопки для изменения настроек
    keyboard = [
        [InlineKeyboardButton("⚠️ Аллергии", callback_data="set_allergies")],
        [InlineKeyboardButton("⏰ Время готовки", callback_data="set_cooking_time")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=settings_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def show_cooking_time_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает опции для выбора времени готовки"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("⏰ Не более 10 минут", callback_data="cooking_time_10")],
        [InlineKeyboardButton("⏰ Не более 20 минут", callback_data="cooking_time_20")],
        [InlineKeyboardButton("⏰ Не более 30 минут", callback_data="cooking_time_30")],
        [InlineKeyboardButton("❌ Убрать фильтр", callback_data="cooking_time_none")],
        [InlineKeyboardButton("🔙 Назад", callback_data="show_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="⏰ <b>Время готовки</b>\n\n"
             "Выберите максимальное время готовки:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def set_cooking_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает время готовки для пользователя"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    
    # Извлекаем время из callback_data
    time_value = query.data.split('_')[-1]
    
    if time_value == "none":
        user_data['preferences']['cooking_time'] = None
        await query.answer("✅ Фильтр времени готовки убран!")
    else:
        time_minutes = int(time_value)
        user_data['preferences']['cooking_time'] = f"Не более {time_minutes} минут"
        await query.answer(f"✅ Установлено время готовки: не более {time_minutes} минут!")
    
    save_user_data(user_id, user_data)
    
    # Возвращаемся к настройкам
    await show_settings(update, context)



def filter_recipes_by_cooking_time(recipes, max_minutes):
    """Фильтрует рецепты по времени готовки"""
    if not max_minutes:
        return recipes
    
    print(f"DEBUG: Фильтрация рецептов по времени готовки (максимум {max_minutes} минут)")
    print(f"DEBUG: Всего рецептов для фильтрации: {len(recipes)}")
    
    filtered_recipes = []
    excluded_recipes = []
    no_time_recipes = []
    
    for recipe in recipes:
        cooking_time = recipe.get('cooking_time', 0)
        if cooking_time == 0:
            # Если время не указано, исключаем рецепт
            no_time_recipes.append(recipe.get('name', 'Unknown'))
        elif cooking_time <= max_minutes:
            filtered_recipes.append(recipe)
        else:
            excluded_recipes.append((recipe.get('name', 'Unknown'), cooking_time))
    
    print(f"DEBUG: Прошло фильтр: {len(filtered_recipes)} рецептов")
    print(f"DEBUG: Исключено по времени: {len(excluded_recipes)} рецептов")
    print(f"DEBUG: Исключено (время не указано): {len(no_time_recipes)} рецептов")
    
    if excluded_recipes:
        print("DEBUG: Исключенные рецепты (превышают время):")
        for name, time in excluded_recipes[:5]:  # Показываем первые 5
            print(f"  - {name}: {time} минут")
    
    if no_time_recipes:
        print("DEBUG: Рецепты без указания времени:")
        for name in no_time_recipes[:5]:  # Показываем первые 5
            print(f"  - {name}")
    
    return filtered_recipes

async def show_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает избранные рецепты пользователя"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    favorites = user_data['favorites']
    
    print(f"DEBUG: Показ избранного для пользователя {user_id}")
    print(f"DEBUG: Избранные рецепты: {favorites}")
    
    if not favorites:
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="⭐ <b>Избранное</b>\n\n"
                 "У вас пока нет избранных рецептов.\n"
                 "Добавляйте понравившиеся рецепты в избранное!",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        return
    
    # Показываем первый избранный рецепт
    recipe_id = favorites[0]
    recipe = next((r for r in RECIPES["recipes"] if r["number"] == recipe_id), None)
    
    if not recipe:
        # Если рецепт не найден, удаляем его из избранного
        favorites.remove(recipe_id)
        save_user_data(user_id, user_data)
        await show_favorites(update, context)
        return
    
    message = format_recipe_message(recipe, 1, len(favorites), user_id)
    
    # Кнопки навигации по избранному
    keyboard = []
    if len(favorites) > 1:
        keyboard.append([
            InlineKeyboardButton("⬅️", callback_data=f"fav_prev_0"),
            InlineKeyboardButton(f"1/{len(favorites)}", callback_data="fav_info"),
            InlineKeyboardButton("➡️", callback_data=f"fav_next_0")
        ])
    
    keyboard.extend([
        [InlineKeyboardButton("🗑️ Удалить из избранного", callback_data=f"remove_fav_{recipe_id}")],
        [InlineKeyboardButton("📋 Получить рецепт", callback_data="show_recipes")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def show_recipes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает три случайных рецепта"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    
    # Проверяем, есть ли рецепты
    if not RECIPES["recipes"]:
        await query.edit_message_text(
            text="❌ Рецепты не найдены. Проверьте файл recipes.json",
            parse_mode='HTML'
        )
        return
    
    # Применяем фильтр по времени готовки
    available_recipes = [r for r in RECIPES["recipes"] if r["number"] not in USED_RECIPE_IDS]
    
    # Получаем настройки времени готовки пользователя
    cooking_time_pref = user_data['preferences']['cooking_time']
    max_minutes = None
    
    if cooking_time_pref:
        # Извлекаем число минут из настройки
        import re
        match = re.search(r'(\d+)', cooking_time_pref)
        if match:
            max_minutes = int(match.group(1))
            available_recipes = filter_recipes_by_cooking_time(available_recipes, max_minutes)
            print(f"DEBUG: Применен фильтр времени готовки: не более {max_minutes} минут")
            print(f"DEBUG: Доступно рецептов после фильтрации: {len(available_recipes)}")
    
    # Если все рецепты были показаны, сбрасываем счетчик
    if len(available_recipes) < 3:
        USED_RECIPE_IDS.clear()
        available_recipes = [r for r in RECIPES["recipes"] if r["number"] not in USED_RECIPE_IDS]
        # Снова применяем фильтр
        if max_minutes:
            available_recipes = filter_recipes_by_cooking_time(available_recipes, max_minutes)
    
    # Проверяем, что у нас достаточно рецептов
    if len(available_recipes) < 3:
        if max_minutes:
            await query.edit_message_text(
                text=f"❌ Недостаточно рецептов для показа с фильтром времени готовки (не более {max_minutes} минут).\n\n"
                     f"Найдено рецептов: {len(available_recipes)}\n"
                     f"Попробуйте изменить фильтр в настройках или убрать его.",
                parse_mode='HTML'
            )
        else:
            await query.edit_message_text(
                text="❌ Недостаточно рецептов для показа. Нужно минимум 3 рецепта.",
                parse_mode='HTML'
            )
        return
    
    selected_recipes = random.sample(available_recipes, 3)
    
    # Отладочная информация о выбранных рецептах
    print(f"DEBUG: Выбрано рецептов: {len(selected_recipes)}")
    for i, recipe in enumerate(selected_recipes):
        cooking_time = recipe.get('cooking_time', 0)
        print(f"DEBUG: Рецепт {i+1}: '{recipe.get('name', 'Unknown')}' - время готовки: {cooking_time} минут")
    
    # Добавляем номер выбранных рецептов в использованные
    for recipe in selected_recipes:
        USED_RECIPE_IDS.add(recipe["number"])
    
    # Показываем первый рецепт
    recipe = selected_recipes[0]
    message = format_recipe_message(recipe, 1, 3, user_id)
    
    # Кнопки навигации
    keyboard = [
        [
            InlineKeyboardButton("⬅️", callback_data="prev_0"),
            InlineKeyboardButton(f"1/3", callback_data="info"),
            InlineKeyboardButton("➡️", callback_data="next_0")
        ],
        [InlineKeyboardButton("⭐ В избранное", callback_data=f"add_fav_{recipe['number']}")],
        [InlineKeyboardButton("🎲 Другие рецепты", callback_data="show_recipes")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Сохраняем выбранные рецепты в контексте
    context.user_data['current_recipes'] = selected_recipes
    
    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )



def format_recipe_message(recipe, current_index, total_count, user_id=None):
    """Форматирует сообщение с рецептом"""
    message = f"📖 <b>{recipe['name']}</b>\n\n"
    
    # Обрабатываем ингредиенты
    ingredients = recipe.get('ingredients', [])
    if isinstance(ingredients, str):
        ingredients_text = ingredients
    elif isinstance(ingredients, list):
        ingredients_text = ', '.join(ingredients)
    else:
        ingredients_text = str(ingredients)
    
    message += f"🥘 <b>Ингредиенты:</b> {ingredients_text}\n"
    
    # Добавляем информацию о времени готовки
    cooking_time = recipe.get('cooking_time', 0)
    if cooking_time > 0:
        message += f"⏰ <b>Время готовки:</b> ~{cooking_time} минут\n"
    
    # Добавляем инструкцию по приготовлению
    method = recipe.get('method', '')
    if method:
        message += f"\n📝 <b>Приготовление:</b>\n{method}\n"
    
    message += f"\n📋 <b>Рецепт #{recipe.get('number', current_index)}</b> из {total_count}\n"
    

    
    return message

async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет рецепт в избранное"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем номер рецепта из callback_data
    recipe_id = int(query.data.split('_')[-1])
    
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    
    print(f"DEBUG: Попытка добавить рецепт {recipe_id} в избранное для пользователя {user_id}")
    print(f"DEBUG: Текущие избранные: {user_data['favorites']}")
    
    if recipe_id not in user_data['favorites']:
        user_data['favorites'].append(recipe_id)
        save_user_data(user_id, user_data)
        print(f"DEBUG: Рецепт {recipe_id} добавлен в избранное. Новый список: {user_data['favorites']}")
        await query.answer("✅ Рецепт добавлен в избранное!")
    else:
        print(f"DEBUG: Рецепт {recipe_id} уже в избранном")
        await query.answer("⚠️ Рецепт уже в избранном!")

async def remove_from_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет рецепт из избранного"""
    query = update.callback_query
    await query.answer()
    
    recipe_id = int(query.data.split('_')[-1])
    
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    
    print(f"DEBUG: Попытка удалить рецепт {recipe_id} из избранного для пользователя {user_id}")
    print(f"DEBUG: Текущие избранные: {user_data['favorites']}")
    
    if recipe_id in user_data['favorites']:
        user_data['favorites'].remove(recipe_id)
        save_user_data(user_id, user_data)
        print(f"DEBUG: Рецепт {recipe_id} удален из избранного. Новый список: {user_data['favorites']}")
        await query.answer("🗑️ Рецепт удален из избранного!")
        
        # Если избранное пустое, возвращаемся в главное меню
        if not user_data['favorites']:
            await main_menu(update, context)
        else:
            # Показываем обновленное избранное
            await show_favorites(update, context)
    else:
        print(f"DEBUG: Рецепт {recipe_id} не найден в избранном")
        await query.answer("⚠️ Рецепт не найден в избранном!")



async def navigate_recipes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Навигация между рецептами"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    current_recipes = context.user_data.get('current_recipes', [])
    
    if not current_recipes:
        await query.answer("❌ Нет доступных рецептов")
        return
    
    # Извлекаем текущий индекс из callback_data
    parts = query.data.split('_')
    direction = parts[0]  # 'prev' или 'next'
    current_index = int(parts[1])
    
    if direction == "prev":
        new_index = (current_index - 1) % len(current_recipes)
    else:  # next
        new_index = (current_index + 1) % len(current_recipes)
    
    recipe = current_recipes[new_index]
    message = format_recipe_message(recipe, new_index + 1, len(current_recipes), user_id)
    
    # Кнопки навигации
    keyboard = [
        [
            InlineKeyboardButton("⬅️", callback_data=f"prev_{new_index}"),
            InlineKeyboardButton(f"{new_index + 1}/{len(current_recipes)}", callback_data="info"),
            InlineKeyboardButton("➡️", callback_data=f"next_{new_index}")
        ],
        [InlineKeyboardButton("⭐ В избранное", callback_data=f"add_fav_{recipe['number']}")],
        [InlineKeyboardButton("🎲 Другие рецепты", callback_data="show_recipes")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def navigate_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Навигация по избранным рецептам"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    favorites = user_data['favorites']
    
    if not favorites:
        await query.answer("❌ Нет избранных рецептов")
        return
    
    # Извлекаем текущий индекс из callback_data
    parts = query.data.split('_')
    direction = parts[1]  # 'prev' или 'next'
    current_index = int(parts[2])
    
    if direction == "prev":
        new_index = (current_index - 1) % len(favorites)
    else:  # next
        new_index = (current_index + 1) % len(favorites)
    
    recipe_id = favorites[new_index]
    recipe = next((r for r in RECIPES["recipes"] if r["number"] == recipe_id), None)
    
    if not recipe:
        # Если рецепт не найден, удаляем его из избранного
        favorites.remove(recipe_id)
        save_user_data(user_id, user_data)
        await query.answer("🗑️ Рецепт удален из избранного (не найден)")
        await show_favorites(update, context)
        return
    
    message = format_recipe_message(recipe, new_index + 1, len(favorites), user_id)
    
    # Кнопки навигации по избранному
    keyboard = []
    if len(favorites) > 1:
        keyboard.append([
            InlineKeyboardButton("⬅️", callback_data=f"fav_prev_{new_index}"),
            InlineKeyboardButton(f"{new_index + 1}/{len(favorites)}", callback_data="fav_info"),
            InlineKeyboardButton("➡️", callback_data=f"fav_next_{new_index}")
        ])
    
    keyboard.extend([
        [InlineKeyboardButton("🗑️ Удалить из избранного", callback_data=f"remove_fav_{recipe_id}")],
        [InlineKeyboardButton("📋 Получить рецепт", callback_data="show_recipes")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает в главное меню"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📋 Получить рецепт", callback_data="show_recipes")],
        [InlineKeyboardButton("⭐ Избранное", callback_data="show_favorites")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="show_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "👋 Главное меню\n\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    
    # Сохраняем user_id в контексте
    context.user_data['user_id'] = query.from_user.id
    
    if query.data == "main_menu":
        await main_menu(update, context)
    elif query.data == "show_recipes":
        await show_recipes(update, context)
    elif query.data == "show_favorites":
        await show_favorites(update, context)
    elif query.data == "show_settings":
        await show_settings(update, context)
    elif query.data.startswith("add_fav_"):
        await add_to_favorites(update, context)
    elif query.data.startswith("remove_fav_"):
        await remove_from_favorites(update, context)

    elif query.data.startswith("prev_") or query.data.startswith("next_"):
        await navigate_recipes(update, context)
    elif query.data.startswith("fav_prev_") or query.data.startswith("fav_next_"):
        await navigate_favorites(update, context)
    elif query.data == "fav_info":
        await query.answer("ℹ️ Информация о навигации по избранному")
    elif query.data == "set_cooking_time":
        await show_cooking_time_options(update, context)
    elif query.data.startswith("cooking_time_"):
        await set_cooking_time(update, context)
    # Добавьте другие обработчики по мере необходимости

def main():
    """Основная функция запуска бота"""
    # Получаем токен бота из переменных окружения (Railway автоматически предоставляет переменные)
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Временное решение - если токен не найден в переменных окружения
    if not token:
        token = "8424689402:AAEWrilYr8sz1JVM6zSvaY3akg0nG029RcM"
        print("⚠️ Используется токен из кода (временное решение)")
    
    if not token:
        print("Ошибка: Не найден токен бота TELEGRAM_BOT_TOKEN")
        print("Установите переменную окружения TELEGRAM_BOT_TOKEN в Railway")
        return
    
    # Проверяем, загрузились ли рецепты
    if not RECIPES["recipes"]:
        print("Ошибка: Рецепты не загружены. Проверьте файл recipes.json")
        return
    
    print(f"✅ Загружено {len(RECIPES['recipes'])} рецептов")
    print(f"🤖 Бот запускается с токеном: {token[:10]}...")
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    print("🚀 Бот запущен и готов к работе!")
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except AttributeError:
        # Альтернативный способ запуска для новых версий
        application.run_polling()
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        raise e

if __name__ == '__main__':
    main()
