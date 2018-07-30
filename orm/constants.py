"""Constants"""
import os
DB_FILE = 'db.sqlite'
DB_URL = 'sqlite:///' + os.path.join(os.path.dirname(__file__), DB_FILE)
