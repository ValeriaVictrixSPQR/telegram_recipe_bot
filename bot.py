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
    
    # Подсчитываем количество рецептов для каждого фильтра
    recipes_10 = len([r for r in RECIPES["recipes"] if r.get('cooking_time', 0) <= 10])
    recipes_20 = len([r for r in RECIPES["recipes"] if r.get('cooking_time', 0) <= 20])
    recipes_30 = len([r for r in RECIPES["recipes"] if r.get('cooking_time', 0) <= 30])
    
    keyboard = [
        [InlineKeyboardButton(f"⏰ Не более 10 минут ({recipes_10} рецептов)", callback_data="cooking_time_10")],
        [InlineKeyboardButton(f"⏰ Не более 20 минут ({recipes_20} рецептов)", callback_data="cooking_time_20")],
        [InlineKeyboardButton(f"⏰ Не более 30 минут ({recipes_30} рецептов)", callback_data="cooking_time_30")],
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
        
        # Подсчитываем количество доступных рецептов
        available_recipes = len([r for r in RECIPES["recipes"] if r.get('cooking_time', 0) <= time_minutes])
        await query.answer(f"✅ Установлено время готовки: не более {time_minutes} минут!\nДоступно рецептов: {available_recipes}")
    
    save_user_data(user_id, user_data)
    
    # Возвращаемся к настройкам
    await show_settings(update, context)



def get_allergy_catalog():
    """Возвращает словарь доступных аллергенов и ключевых слов для поиска в ингредиентах."""
    return {
        'молочные продукты': [
            'молоко', 'сливк', 'сливочн', 'творог', 'творож', 'сыр', 'йогурт', 'кефир', 'маскарпон', 'сметан'
        ],
        'яйца': [
            'яйц', 'желток', 'белок', 'перепели'
        ],
        'глютен (пшеница)': [
            'пшен', 'мука', 'вермиш', 'лапша', 'макарон', 'спагетти', 'паста', 'батон', 'хлеб'
        ],
        'орехи/арахис': [
            'орех', 'миндаль', 'грецк', 'фундук', 'кешью', 'арахис', 'арахисовая паста', 'миндальн'
        ],
        'рыба/морепродукты': [
            'рыба', 'лосось', 'семга', 'треска', 'хек', 'тунец', 'форель', 'султанка', 'кревет'
        ],
        'соя': [
            'соя', 'соев'
        ],
        'кунжут/тахини': [
            'кунжут', 'тахин'
        ],
        'мёд': [
            'мёд', 'мед '
        ]
    }

def format_allergies_text(selected: list) -> str:
    return ", ".join(selected) if selected else "не указаны"

async def show_allergies_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает опции выбора аллергенов (переключатели)."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    selected = set(user_data['preferences'].get('allergies', []))

    catalog = get_allergy_catalog()

    # Формируем клавиатуру с переключателями
    keyboard = []
    for allergy_name in catalog.keys():
        checked = '✅ ' if allergy_name in selected else ''
        keyboard.append([InlineKeyboardButton(f"{checked}{allergy_name}", callback_data=f"allergy_toggle_{allergy_name}")])

    keyboard.append([InlineKeyboardButton("🧹 Очистить", callback_data="allergy_clear")])
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="show_settings")])

    text = (
        "⚠️ <b>Аллергии</b>\n\n"
        f"Текущие: {format_allergies_text(list(selected))}\n\n"
        "Нажимайте, чтобы включить/выключить аллерген."
    )

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def toggle_allergy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Переключает аллерген в списке пользователя."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    prefs = user_data['preferences']

    # Имя аллергена идёт после allergy_toggle_
    allergy_name = query.data[len('allergy_toggle_'):]

    current = set(prefs.get('allergies', []))
    if allergy_name in current:
        current.remove(allergy_name)
    else:
        current.add(allergy_name)
    prefs['allergies'] = list(current)
    save_user_data(user_id, user_data)

    # Обновляем экран выбора аллергий
    await show_allergies_options(update, context)

async def clear_allergies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очищает все выбранные аллергены."""
    query = update.callback_query
    await query.answer("Аллергии очищены")

    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    user_data['preferences']['allergies'] = []
    save_user_data(user_id, user_data)

    await show_allergies_options(update, context)

def filter_recipes_by_allergies(recipes, selected_allergies):
    """Исключает рецепты, содержащие выбранные аллергены в ингредиентах."""
    if not selected_allergies:
        return recipes

    catalog = get_allergy_catalog()

    # Собираем ключевые слова по выбранным аллергенам
    keywords = []
    for allergy_name in selected_allergies:
        keywords.extend(catalog.get(allergy_name, []))

    def recipe_is_safe(recipe) -> bool:
        ingredients_text = (recipe.get('ingredients') or '').lower()
        # если какое-либо ключевое слово встречается в ингредиентах — рецепт не подходит
        for kw in keywords:
            if kw.lower() in ingredients_text:
                return False
        return True

    filtered = [r for r in recipes if recipe_is_safe(r)]
    return filtered

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
            # Дополнительная проверка
            if cooking_time > max_minutes:
                print(f"ERROR: Рецепт '{recipe.get('name', 'Unknown')}' прошел фильтр, но время {cooking_time} > {max_minutes}")
        else:
            excluded_recipes.append((recipe.get('name', 'Unknown'), cooking_time))
    
    print(f"DEBUG: Прошло фильтр: {len(filtered_recipes)} рецептов")
    print(f"DEBUG: Исключено по времени: {len(excluded_recipes)} рецептов")
    print(f"DEBUG: Исключено (время не указано): {len(no_time_recipes)} рецептов")
    
    # Финальная проверка всех отфильтрованных рецептов
    for recipe in filtered_recipes:
        cooking_time = recipe.get('cooking_time', 0)
        if cooking_time > max_minutes:
            print(f"ERROR: В отфильтрованных рецептах найден неподходящий: '{recipe.get('name', 'Unknown')}' - время {cooking_time} минут")
    
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
    
    # Получаем настройки фильтров пользователя
    cooking_time_pref = user_data['preferences']['cooking_time']
    max_minutes = None
    selected_allergies = user_data['preferences'].get('allergies', [])
    
    if cooking_time_pref:
        # Извлекаем число минут из настройки
        import re
        match = re.search(r'(\d+)', cooking_time_pref)
        if match:
            max_minutes = int(match.group(1))
            print(f"DEBUG: Установлен фильтр времени готовки: не более {max_minutes} минут")
    
    # 1) Фильтр по времени готовки ко ВСЕМ рецептам
    if max_minutes:
        base_filtered = filter_recipes_by_cooking_time(RECIPES["recipes"], max_minutes)
        print(f"DEBUG: Всего рецептов с фильтром {max_minutes} минут: {len(base_filtered)}")
    else:
        base_filtered = list(RECIPES["recipes"])  # копия списка

    # 2) Фильтр по аллергенам
    if selected_allergies:
        before = len(base_filtered)
        base_filtered = filter_recipes_by_allergies(base_filtered, selected_allergies)
        print(f"DEBUG: Аллергии выбраны: {selected_allergies}. До: {before}, после: {len(base_filtered)}")

    # 3) Убираем уже показанные рецепты
    available_recipes = [r for r in base_filtered if r["number"] not in USED_RECIPE_IDS]
    print(f"DEBUG: Доступно рецептов после всех фильтров: {len(available_recipes)}")
    
    # Если все рецепты были показаны, сбрасываем счетчик и применяем фильтр заново
    if len(available_recipes) < 3:
        print(f"DEBUG: Недостаточно доступных рецептов ({len(available_recipes)}), сбрасываем счетчик")
        USED_RECIPE_IDS.clear()
        
        # Применяем те же фильтры заново к полной базе
        base_filtered = RECIPES["recipes"]
        if max_minutes:
            base_filtered = filter_recipes_by_cooking_time(base_filtered, max_minutes)
        if selected_allergies:
            base_filtered = filter_recipes_by_allergies(base_filtered, selected_allergies)
        available_recipes = base_filtered
        print(f"DEBUG: После сброса доступно рецептов после фильтров: {len(available_recipes)}")
    
    # Проверяем, что у нас достаточно рецептов
    if len(available_recipes) < 3:
        if max_minutes:
            # Показываем информацию о фильтре и предлагаем альтернативы
            total_with_filter = len([r for r in RECIPES["recipes"] if r.get('cooking_time', 0) <= max_minutes])
            message = f"❌ <b>Недостаточно рецептов с фильтром времени готовки</b>\n\n"
            message += f"⏰ Фильтр: не более {max_minutes} минут\n"
            message += f"📊 Найдено рецептов: {len(available_recipes)}\n"
            message += f"📊 Всего рецептов с этим фильтром: {total_with_filter}\n\n"
            message += f"💡 <b>Рекомендации:</b>\n"
            message += f"• Увеличьте время готовки в настройках\n"
            message += f"• Уберите фильтр времени готовки\n"
            message += f"• Проверьте фильтры аллергенов"
            
            keyboard = [
                [InlineKeyboardButton("⚙️ Настройки", callback_data="show_settings")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=message,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
        else:
            await query.edit_message_text(
                text="❌ Недостаточно рецептов для показа. Нужно минимум 3 рецепта.",
                parse_mode='HTML'
            )
        return
    
    # Выбираем 3 случайных рецепта
    selected_recipes = random.sample(available_recipes, 3)
    
    # Финальная проверка: соответствие всем фильтрам
    if max_minutes or selected_allergies:
        print("DEBUG: Финальная проверка активных фильтров")
        for recipe in selected_recipes:
            if max_minutes:
                cooking_time = recipe.get('cooking_time', 0)
                if cooking_time == 0 or cooking_time > max_minutes:
                    print(f"ERROR: Несоответствие времени: {recipe.get('name')} {cooking_time} > {max_minutes}")
            if selected_allergies:
                ing = (recipe.get('ingredients') or '').lower()
                for allergy_name, kws in get_allergy_catalog().items():
                    if allergy_name in selected_allergies:
                        if any(kw.lower() in ing for kw in kws):
                            print(f"ERROR: Рецепт содержит аллерген '{allergy_name}': {recipe.get('name')}")
    
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
    
    message += f"🥘 <b>Ингредиенты:</b> {ingredients_text}\n\n"
    
    # Добавляем инструкцию по приготовлению
    method = recipe.get('method', '')
    if method:
        message += f"📝 <b>Приготовление:</b>\n{method}\n\n"
    
    # Добавляем информацию о времени готовки в конце
    cooking_time = recipe.get('cooking_time', 0)
    if cooking_time > 0:
        message += f"⏰ <b>Время готовки:</b> ~{cooking_time} минут"
    

    
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
    elif query.data == "set_allergies":
        await show_allergies_options(update, context)
    elif query.data.startswith("allergy_toggle_"):
        await toggle_allergy(update, context)
    elif query.data == "allergy_clear":
        await clear_allergies(update, context)
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
