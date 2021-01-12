from flask import g


def function_accessing_global():
    return g.token
