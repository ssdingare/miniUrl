#!env/bin/python
from miniUrl import app, init_db
import argparse

parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--init', action='store_true', help='initialize for first use')
args = parser.parse_args()

if args.init:
    with app.app_context():
        init_db()

app.run(debug=True)

