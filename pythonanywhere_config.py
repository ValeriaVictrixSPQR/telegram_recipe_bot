#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Конфигурация для PythonAnywhere
Этот файл содержит настройки для размещения приложения на PythonAnywhere
"""

import os
from web_app import app

# Настройки для PythonAnywhere
if __name__ == '__main__':
    # Для локальной разработки
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Для PythonAnywhere - экспортируем приложение
    application = app

