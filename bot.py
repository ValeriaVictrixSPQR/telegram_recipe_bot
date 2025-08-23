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

# Глобальная переменная для хранения рецептов
RECIPES = load_recipes()
USED_RECIPE_IDS = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Рецепты", callback_data="show_recipes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Привет! Я бот с рецептами. Нажми на кнопку 'Рецепты' чтобы получить три случайных рецепта!",
        reply_markup=reply_markup
    )

async def show_recipes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает три случайных рецепта"""
    query = update.callback_query
    await query.answer()
    
    # Проверяем, есть ли рецепты
    if not RECIPES["recipes"]:
        await query.edit_message_text(
            text="❌ Рецепты не найдены. Проверьте файл recipes.json",
            parse_mode='HTML'
        )
        return
    
    # Получаем три случайных рецепта
    available_recipes = [r for r in RECIPES["recipes"] if r["number"] not in USED_RECIPE_IDS]
    
    # Если все рецепты были показаны, сбрасываем счетчик
    if len(available_recipes) < 3:
        USED_RECIPE_IDS.clear()
        available_recipes = RECIPES["recipes"]
    
    # Проверяем, что у нас достаточно рецептов
    if len(available_recipes) < 3:
        await query.edit_message_text(
            text="❌ Недостаточно рецептов для показа. Нужно минимум 3 рецепта.",
            parse_mode='HTML'
        )
        return
    
    selected_recipes = random.sample(available_recipes, 3)
    
    # Добавляем номер выбранных рецептов в использованные
    for recipe in selected_recipes:
        USED_RECIPE_IDS.add(recipe["number"])
    
    # Формируем сообщение с рецептами
    message = "🍽️ Вот три рецепта для вас:\n\n"
    
    for i, recipe in enumerate(selected_recipes, 1):
        message += f"📖 <b>{i}. {recipe['name']}</b>\n"
        
        # Обрабатываем ингредиенты (могут быть строкой или списком)
        ingredients = recipe.get('ingredients', [])
        if isinstance(ingredients, str):
            ingredients_text = ingredients
        elif isinstance(ingredients, list):
            ingredients_text = ', '.join(ingredients)
        else:
            ingredients_text = str(ingredients)
        
        message += f"🥘 <b>Ингредиенты:</b> {ingredients_text}\n"
        message += f"📝 <b>Приготовление:</b> {recipe.get('method', 'Инструкция не указана')}\n\n"
    
    # Кнопка для получения других рецептов
    keyboard = [
        [InlineKeyboardButton("Давай другое", callback_data="show_recipes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        # Если не удалось отредактировать, отправляем новое
        await query.message.reply_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    
    if query.data == "show_recipes":
        await show_recipes(update, context)

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
