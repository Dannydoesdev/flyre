import psycopg2
import os
import bcrypt

from flask import Flask, request, redirect, render_template, session

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=flyre')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret key for testing')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY



@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT * from USERS')
    results = cur.fetchall()
    print(results)
    # email = session.get('email')
    # name = session.get('name')
    # id = session.get('id')
    # if email:
    #     print(email)
    # if name:
    #     print(name)
    # if id:
    #     print(id)

    return render_template('index.html', results=results)

    # conn = psycopg2.connect(DATABASE_URL)
    # cur =  conn.cursor()
    # cur.execute('SELECT 1', [])
    # conn.close()
    
    # return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)