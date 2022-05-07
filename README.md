## FLYRE app

### Connecting local talent to local events

### Live site

### [Find the live site by clicking here](https://morning-atoll-11830.herokuapp.com/)


### Contact

You can find me at [Linkedin](https://www.linkedin.com/in/danieltmcgee/)

### General Assembly Project 2


### User stories:

As a DJ I want to promote myself to party organisers so that they can find me, hear my music and book me

As a party/club/festival organiser I want to be able to easily search out DJs, find their music, genre, location, prices etc and contact them so that I can run a successful event


### Features:

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
- Using dictionaries to go through to the Jinja to make it readable
- Import and update bootstrap on all pages
- Send through iframes to the HTML and allow them to show up


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

### Add Soundcloud page:
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

### Soundcloud API fn:
#### When called - send the parameters to the embed API which returns an iframe (or error if not)
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

### Display Soundcloud iframes on page
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

### Main Challenges:


## Things I'd like to do in future:

- More mobile friendly
- Allow artists to add past events & locations played
- Review functionality
- instagram/FB/Youtube API functionality for photos/events/videos
- Search functionality
- Cloud image upload
- Improve onboarding flow
- Forgot pwd


### Known bugs/issues

- User needs to update every field in 'profile update screen', should be optional which gets updated
- Currently no limitation on character count (move to VARCHAR(##) columns in schema)
- Not any great error handling for user (existing email etc)




### OLD README:


## Concept (unless I pivot):

Connect DJs(& artists) with clubs/parties/promoters etc


### Optional extra concept:
(DJs slash artists?)

To define ‘artists’ scope (bands/performers etc) - focus on DJs for now?


### Features:

Login for DJs

Bio, links, picture, contact info, location

Search page

- Search filters:
- Genre
- Location
- Price
- Reviews

### Optional freatures:

Login for organisers

Reviews (recommendations?)

Prices

Host music on site


### Technicals:

Homepage when not logged in

Homepage when logged in

Individual pages for DJs

Database for users (DJs)

Database for bios, profile picture, links etc

### Optional technicals:

Individual pages for organisers

Database for users (organisers)

Dynamic database for reviews
