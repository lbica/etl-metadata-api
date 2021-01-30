"""
This is for production
"""


import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
