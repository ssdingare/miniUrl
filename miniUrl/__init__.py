import sqlite3
from flask import Flask, g

app = Flask(__name__)
app.config.from_object('config')


def get_db():
    """
    Return db connection for given app context g or instantiate if none
    """
    if not hasattr(g, 'db'):
        g.db = connect_db(app.config['DATABASE'])
    return g.db


def connect_db(path):
    return sqlite3.connect(path)


def init_db():
    """
    Initialize database using schema file and populate the device types
    """
    db = get_db()
    with app.open_resource(app.config['SCHEMA'], mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()


@app.cli.command('init')
def init_command():
    init_db()


@app.teardown_appcontext
def close(error):
    """
    Close database connection on teardown
    """
    if hasattr(g, 'db'):
        g.db.close()


from miniUrl import views

