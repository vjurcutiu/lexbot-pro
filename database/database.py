import sqlite3
from flask import g
import os

DATABASE = 'main.db'

def get_db():
    """
    Opens a new database connection if there is none yet for the current app context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Optional: Return rows as dictionaries
    return g.db

def close_db(exception=None):
    """
    Closes the database connection if it exists.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()