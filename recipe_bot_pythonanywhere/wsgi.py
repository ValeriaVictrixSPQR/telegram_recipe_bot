#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WSGI файл для PythonAnywhere
Этот файл должен быть указан в настройках веб-приложения PythonAnywhere
"""

import sys
import os

# Добавляем путь к проекту в sys.path
# Замените 'yourusername' на ваше имя пользователя PythonAnywhere
project_path = '/home/SlapMeSalami/recipe_bot'
if project_path not in sys.path:
    sys.path.append(project_path)

# Импортируем Flask приложение
from web_app import app as application

# Для отладки (можно убрать в продакшене)
if __name__ == '__main__':
    application.run()

