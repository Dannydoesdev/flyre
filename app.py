import psycopg2

from flask import Flask
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=project2')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret key for testing')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
    cur =  conn.cursor()
    cur.execute('SELECT 1', [])
    conn.close()
    
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)