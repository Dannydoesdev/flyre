## FLYRE app

### Connecting local talent to local events

## Live site

### [Find the live site by clicking here](https://morning-atoll-11830.herokuapp.com/)


## Contact

You can find me at [Linkedin](https://www.linkedin.com/in/danieltmcgee/)


## Languages used:

Python
Flask
Jinja
HTML
CSS
Bootstrap
Javascript


## Process:

Ideation - Started with multiple ideas and decided to go with a friends suggestion, based on the 'fyre' app that the 'fyre' festival was promoting. Connect DJs with organisers

Research - Spoke with local artists and event organisers, sent out a [survey to relevant user types](https://forms.gle/Ff2J9qaimaYMkKpv7)

Scope - Used MOSCOW to decide on priority features to have a solid working MVP

Code - Spent most of my time getting the infrastructure working (API returns, flask sending correct info to templates etc) before moving on to design

Design - Researched similar sites (especially Soundcloud, where artists would be familiar), [used Figma to draw up wireframes] (https://www.figma.com/file/K4HYl8z5A7Ajd0Elbadnva/Flyre?node-id=24%3A2075)

Implementing designs - Decided to learn and apply bootstrap after running into limitations with what I wanted to achieve with a consistent look and feel in CSS. Used custom styling within bootstrap to get the look I wanted


## User stories:

As a DJ I want to promote myself to party organisers so that they can find me, hear my music and get in contact with me

As a party/club/festival organiser I want to be able to easily find an search local artists to play events


## Features:

- Artist signup
- Artist login
- Featured artists
- Copy Soundcloud link to return iframe on artist page
- Bootstrap layout
- Artist list page
- Logic to detect user logged in/on their own page


## Code:

3 tables - 
- User for all unique info
- Tracks - saved soundcloud urls (literally iframes)
- Genres - for multiple genres

(all these reference users(user_id))

Other stuff - 
- Passing dictionaries to Jinja to make code more readable
- Import and updated bootstrap on all pages
- Send iframes from SQL to an API through to HTML and display on page


## Artist page:
#### Check if id in args matches id in cookie to show user-specific artist page functionality

#### Create list of the track URLs in the tracks table, use get_track fn to return the iframes from API
#### Append each iframe HTML to list and send through template to parse in jinja


```python

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
        track_url = response[0]
        for one_response in response:
            track_response_list.append(one_response[0])

    else:
        track_url = ''

    iframe_list = []

    if track_url:
        iframe = get_track(track_url)
        for url in track_response_list:
            iframe_list.append(get_track(url))
    else:
        iframe = ''


    if str(session.get('id')) == request.args.get('id'):
        current_user = 'yep'
    else:
        current_user = 'not'

    cur.execute('SELECT * FROM USERS WHERE user_id = %s', [id])
    response = cur.fetchall()
    results = response[0]


    cur.execute('SELECT genre_name FROM genres WHERE user_id = %s', [id])
    genres = cur.fetchall()


    return render_template('artist.html', results=results, genres=genres, current_user=current_user, iframe=iframe, iframe_list=iframe_list)

```

## Add Soundcloud page:
#### Send through to action page where get_track fn is called
#### If not null (calculated in get_track) update the tracks table with the url

```python

@app.route('/add_soundcloud')
def add_soundcloud():
    return render_template('add_soundcloud.html', name=session.get('name'))


@app.route('/add_soundcloud_action', methods=['POST'])
def add_soundcloud_action():
    id=session.get('id')
    track_url = request.form.get('track_url')
    sc_response = get_track(track_url)
    if sc_response:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('INSERT INTO tracks (track_url, user_id) VALUES (%s, %s)', (track_url, id))
        conn.commit()

        cur.execute('SELECT track_url from tracks where user_id = %s', [id])
        response = cur.fetchone()
        track_url = response[0]
        conn.close()

    else:

        print('track not found!')

    return redirect(f'/artist?id={id}')

```

## Soundcloud API fn:
#### When called - send the parameters to the embed API which returns an iframe (or null if not)
#### Function then returns that iframe response

```python

import requests

EMBED_URL = "https://soundcloud.com/oembed"

def get_track(track_url):
    params = {
        'format': 'json',
        'url': track_url
    }

    response = requests.get(EMBED_URL, params=params)


    if '200' in str(response):
        print('OK')
        response_json = response.json()
        html = response_json['html']
    else:
        print('NOT OK')
        html = ''


    return html

```

## Display Soundcloud iframes on page:
#### Loop through iframe list that is sent and display with |safe (as Flask will filter it out otherwise)
#### Allows for multiple tracks to be shown on page

```python

<div class="container-fluid bg-dark text-white artist_music_bio">
    <div class="row">
        <div class="col-8 artist_music">

            <h4>Artist music</h4>
            {% if iframe_list %}
            {% for item in iframe_list %}
            {{ item|safe }}<br><br>
            {% endfor %}
       
            {% else %}

            <p>{{ results[2] }} hasn't uploaded any tracks yet</p>

            {% endif %}

        </div>

```


## Artist list page:

#### Send a dictionary - make it much more readable in the jinja templates
#### Using 2 different tables - able to calculate in the jinja that they user_ids match (as they reference eachother)
#### Allows the genres to append to the right user

```python

<div class="artist_list_all">

  {% for artist in artist_list_response %}
  <div class='artist_list_div'>
    <a class='artist_list_inner' href='/artist?id={{ artist.user_id }}'>
      <div class="artist_list_name_genre">
        <h4>{{ artist.name }}</h4>
        <div class='artist_list_genres'>

          {# Append genres of artist if the genres table matches users table user_id #}

          {% for genre_list in genre_list_response %}
          {% if genre_list.user_id == artist.user_id %}
          <p>{{ genre_list.genre_name }}</p>
          {% endif %}
          {% endfor %}
        </div>
      </div>
      {% if artist.profile_photo_url %}
      <img class='artist_list_img' src="{{ artist.profile_photo_url }}"></img>
      {% else %}
      <img class='artist_list_noimg' src="../static/img/placeholder-1.jpg"></img>

      {% endif %}

    </a>
  </div>
  {% endfor %}

</div>

{% endblock %}

</div>


```
## Adding genres page:

#### Some checks to make sure existing genres aren't duplicated when using checkboxes
#### Using a list conditional to pull all the existing genres from the table
#### Using a form.getlist to pull all values from the user submission
#### Looping over the .getlist return to make sure each isn't in the table, then insterting

```python


@app.route('/add_genres')
def add_genres():
    return render_template('add_genres.html', name=session.get('name'))


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



```


## Main Challenges:

- Soundcloud no longer creates API keys for their main API, however I was able to use oembed to return code I could use as an iframe on the site
- Pivoting to bootstrap for the desired CSS layouts half way through, meant a lot of re-factoring but turned out well
- Getting consistent pleasant design/UX across all the pages was a lot of work, I'm glad with how it looks but ended up with less time for more features

## Things I'd like to do in future:

- More mobile friendly
- Allow artists to add past events & locations played
- Review functionality
- instagram/FB/Youtube API functionality for photos/events/videos
- Search functionality
- Cloud image upload
- Improve onboarding flow
- Forgot pwd


## Known bugs/issues

- User needs to update every field in 'profile update screen', should be optional to fill out the ones you want
- Currently no limitation on character count (move to VARCHAR(##) columns in schema)
- Not any great error handling for user (existing email etc)
         - Note: Created error page for incorrect pwds

