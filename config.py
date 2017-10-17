from os.path import abspath, join, dirname
from miniUrl import app

basedir = abspath(dirname(__file__))

DATABASE = join(app.root_path, 'miniURL.db')
USERNAME = 'admin'
PASSWORD = 'default'
SCHEMA = 'schema.sql'
