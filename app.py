import psycopg2
import os
import bcrypt

from psycopg2.extras import RealDictCursor

from functions import *
from scapi import get_track

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
    name = session.get('name')
    id = session.get('id')

    print(results)
    
    return render_template('index.html', results=results, name=name, id=id, username=session.get('name'))


@app.route('/artist_list')
def artist_list():
    artist_list_response = sql_fetch('SELECT user_id, name, profile_photo_url FROM users')

    genre_list_response = sql_fetch('SELECT * FROM genres')
    print(genre_list_response)
    return render_template('artist_list.html', name=session.get('name'), artist_list=artist_list, artist_list_response=artist_list_response, genre_list_response=genre_list_response)


@app.route('/artist', methods=['GET'])
def artist():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    id = request.args.get('id')
    cookie = session.get('id')
    arg = request.args.get('id')

    if str(cookie) == arg:
        current_user = True

    cur.execute('SELECT track_url from tracks where user_id = %s', [id])
    response = cur.fetchall()
    
    track_response_list = []

    if response:
        print(response)
        track_url = response[0]
        for one_response in response:
            print(one_response[0])
            track_response_list.append(one_response[0])

    else:
        track_url = ''

    iframe_list = []

    if track_url:
        print(track_url)
        iframe = get_track(track_url)
        for url in track_response_list:
            iframe_list.append(get_track(url))
    else:
        iframe = ''

    print(iframe_list)
    for item in iframe_list:
        print(item)


    if str(session.get('id')) == request.args.get('id'):
        current_user = 'yep'
    else:
        current_user = 'not'

    cur.execute('SELECT * FROM USERS WHERE user_id = %s', [id])
    response = cur.fetchall()
    results = response[0]

    cur.execute('SELECT * FROM USERS WHERE user_id = %s', [id])
    response_one = cur.fetchone()
    results_one = response[0]
    user_id = results[1]
    artist_name = results[2]
    location = results[3]
    profile_photo = results[6]
    background_image = results[7]
    soundcloud_url = results[8]
    facebook_url = results[9]
    bio = results[4]
    email = results[5]


    cur.execute('SELECT genre_name FROM genres WHERE user_id = %s', [id])
    genres = cur.fetchall()

    print(genres)
    for genre in genres:
        print(genre)

    return render_template('artist.html', results=results, genres=genres, current_user=current_user, iframe=iframe, iframe_list=iframe_list) 


@app.route('/error')
def error():
    return render_template('error.html', name=session.get('name'))


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
                return redirect('/error')
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
        session['email'] = email
        
        conn.commit()

        cur.execute('SELECT user_id from users where email = %s', [email])
        response = cur.fetchone()
        id = response[0]
        print(id)
        print('testing result')
        session['id'] = id
        conn.close()
 
    return redirect(f'/artist?id={id}')

@app.route('/register')
def register():
    return render_template('register.html', name=session.get('name'))


@app.route('/add_soundcloud_action', methods=['POST'])
def add_soundcloud_action():
    id=session.get('id')
    track_url = request.form.get('track_url')
    sc_response = get_track(track_url)
    if sc_response:
        print('track found!')
        print(sc_response)
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('INSERT INTO tracks (track_url, user_id) VALUES (%s, %s)', (track_url, id))
        conn.commit()

        cur.execute('SELECT track_url from tracks where user_id = %s', [id])
        response = cur.fetchone()
        track_url = response[0]
        print(id)
        print('testing result')
        conn.close()

    else:

        print('track not found!')

    return redirect(f'/artist?id={id}')


@app.route('/add_soundcloud')
def add_soundcloud():
    return render_template('add_soundcloud.html', name=session.get('name'))

@app.route('/complete_profile_action', methods=['POST'])
def complete_profile_action():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    location = request.form.get('location')
    bio = request.form.get('bio')
    profile_photo_url = request.form.get('profile_photo_url')
    soundcloud_url = request.form.get('soundcloud_url')
    facebook_url = request.form.get('facebook_url')
    user_type = request.form.get('user_type')

    id = session.get('id')

    cur.execute('UPDATE users SET(location, bio, profile_photo_url, soundcloud_url, facebook_url, user_type) = (%s, %s, %s, %s, %s, %s) WHERE user_id = %s', (location, bio, profile_photo_url, soundcloud_url, facebook_url, user_type, id))

    
    conn.commit()

    conn.close()
 
    return redirect(f'/artist?id={id}')

@app.route('/complete_profile')
def complete_profile():
    return render_template('complete_profile.html', name=session.get('name'))


@app.route('/add_genres_action', methods=['POST'])
def add_genres_action():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    chosen_genres = request.form.getlist('genres')
    id = session.get('id')
    genre_check = sql_fetch('SELECT genre_name FROM genres WHERE user_id = %s', [id])
    existing_genre_list = [genre_check['genre_name'] for genre_check in genre_check]

    for genre in chosen_genres:
        if genre not in existing_genre_list:
            print('genre not found')
            sql_write('INSERT INTO genres (user_id, genre_name) VALUES (%s, %s)', (id, genre))
        else:
            print('genre found')

    conn.commit()
    conn.close()
 
    return redirect(f'/artist?id={id}')

@app.route('/add_genres')
def add_genres():
    return render_template('add_genres.html', name=session.get('name'))


if __name__ == '__main__':
    app.run(debug=True)

   