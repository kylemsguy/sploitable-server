import sqlite3
from sqlite3 import Error
from flask import Flask, abort, request

app = Flask(__name__)

conn = sqlite3.connect(':memory:')
c = conn.cursor()

def init_db():
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user TEXT, 
            pass TEXT
        )
    ''')

    c.execute('''
        INSERT INTO users (user, pass) VALUES (
            'Captain Falcon', ''
        )
    ''')

    conn.commit()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "GET is not supported on this endpoint"

    if request.method == 'POST':
        data = request.get_json(force=True, silent=True)

        if not data:
            # 400 Bad Request
            abort(400)
        
        user = data.get('user')
        password = data.get('pass')

        if not (user and password):
            # pls give me user and pass
            abort(400)

        # Sketchy code incoming
        q = "SELECT id from users WHERE user = '" + user + "' AND pass = '" + password + "'"
        c.execute(q)
        result = c.fetchone()

        if result:
            return "flag(YouGotBoostPower)"

        abort(401)

init_db()

if __name__ == '__main__':
    app.run()