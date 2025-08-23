#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для локального тестирования веб-приложения
"""

from web_app import app

if __name__ == '__main__':
    print("🚀 Запуск веб-приложения с рецептами...")
    print("📱 Откройте браузер и перейдите по адресу: http://localhost:8080")
    print("🛑 Для остановки нажмите Ctrl+C")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено")

