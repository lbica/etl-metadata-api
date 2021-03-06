"""
This is for development. The config.py will override the values for production
"""

import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
SECRET_KEY = os.getenv("APP_SECRET_KEY")