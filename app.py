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
    name = session.get('name')
    id = session.get('id')

    return render_template('index.html', results=results, name=name, id=id, username=session.get('name'))

@app.route('/artist', methods=['GET'])
def artist():
    id = request.args.get('id')
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT * FROM USERS WHERE user_id = %s', [id])
    response = cur.fetchall()
    results = response[0]

    cur.execute('SELECT genre_name FROM genres WHERE user_id = %s', [id])
    genres = cur.fetchall()
    # print(genre_response)
    # genres = genre_response[0]
    print(genres)
    for genre in genres:
        print(genre)

    return render_template('artist.html', results=results, genres=genres) 

@app.route('/login')
def login():
    return render_template('login.html', name=session.get('name'))

@app.route('/login_action', methods=['POST'])
def login_action():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT name, email, hashed_password from users')
    user_emails = cur.fetchall()
    print(user_emails)
    email = request.form.get('email')
    print(email)
    password = request.form.get('password')
    for item in user_emails:
        if email in item:
            print('email found!')
            cur.execute('SELECT name, user_id, hashed_password from users where email = %s', [email])
            response = cur.fetchone()
            name = response[0]
            print(name)
            id = response[1]
            print(id)
            password_hash = response[2]
            valid = bcrypt.checkpw(password.encode(), password_hash.encode())
            if valid:
                print('password correct!!')
                session['email'] = email
                session['name'] = name
                session['id'] = id

        else:
            print('email not found')
   
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/register_action', methods=['POST'])
def register_action():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    cur.execute('SELECT * from users WHERE email = %s', [email])
    email_check = cur.fetchall()

    if email_check:
        print('email already exists')
    else:
        print('email does not exist')
        hash_pass = bcrypt.hashpw(f'{password}'.encode(), bcrypt.gensalt()).decode()
        print(hash_pass)
        cur.execute('INSERT INTO users (hashed_password, email, name) VALUES (%s, %s, %s)', (hash_pass, email, name))
        session['name'] = name
        conn.commit()
        conn.close()
    
    
   
    return redirect('/')


@app.route('/register')
def register():
    return render_template('register.html', name=session.get('name'))

if __name__ == '__main__':
    app.run(debug=True)