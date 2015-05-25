# -*- coding: utf-8 -*-
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

Config = {
    'secret_key': os.environ.get('SECRET_KEY'),
}
