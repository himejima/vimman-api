# -*- coding: utf-8 -*-
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

Config = {
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'DATABASE_URL': os.environ.get('DATABASE_URL')
}
