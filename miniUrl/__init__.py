import sqlite3
from flask import Flask, g

app = Flask(__name__)
app.config.from_object('config')


def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db(app.config['DATABASE'])
    return g.db


def connect_db(path):
    try:
        conn = sqlite3.connect(path)
        return conn
    except sqlite3.Error as error:
        print(error)
        exit()


def init_db():
    db = get_db()
    with app.open_resource(app.config['SCHEMA'], mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()


@app.cli.command('init')
def init_command():
    init_db()


@app.teardown_appcontext
def close(error):
    if hasattr(g, 'db'):
        g.db.close()


from miniUrl import views

