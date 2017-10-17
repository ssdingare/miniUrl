from os.path import abspath, join, dirname
from miniUrl import app

basedir = abspath(dirname(__file__))

DATABASE = join(app.root_path, 'miniURL.db')
USERNAME = 'admin'
PASSWORD = 'default'
SCHEMA = 'schema.sql'
MINI_URL_BASE = 'http://localhost:5000/mini/'
