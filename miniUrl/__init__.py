import sqlite3
from os.path import join
from flask import Flask, g

app = Flask(__name__)

db_dir = join(app.root_path, 'db')
app.config.update(dict(
    DATABASE=join(db_dir, 'miniURL.db'),
    USERNAME='admin',
    PASSWORD='default',
    SCHEMA=join(db_dir, 'schema.sql'),
    MINI_URL_BASE='http://localhost:5000/mini/'
))


def get_db():
    """
    Return db connection for given app context g or instantiate if none
    """
    if not hasattr(g, 'db'):
        g.db = connect_db(app.config['DATABASE'])
    return g.db


def connect_db(path):
    """
    Connect in auto-commit mode
    """
    return sqlite3.connect(path, isolation_level=None)


def init_db():
    """
    Initialize database using schema file and populate the device types
    """
    db = get_db()
    with app.open_resource(app.config['SCHEMA'], mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()


@app.teardown_appcontext
def close(error):
    """
    Close database connection on teardown
    """
    if hasattr(g, 'db'):
        g.db.close()


from miniUrl import views

