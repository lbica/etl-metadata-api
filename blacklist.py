"""
blacklist.py

This file juts contains the blacklist of the JWT tokens. it will be imported by app and the logout resource so that
tokens can be added to the blacklist when the user log out.
"""


BLACKLIST = set()
