from os.path import abspath, join, dirname
from miniUrl import app

db_dir = join(app.root_path, 'db')

DATABASE = join(db_dir, 'miniURL.db')
USERNAME = 'admin'
PASSWORD = 'default'
SCHEMA = join(db_dir, 'schema.sql')
MINI_URL_BASE = 'http://localhost:5000/mini/'
