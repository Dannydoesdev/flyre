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
- Copy Soundcloud link to present on page
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

### Artist page:
#### Check if id in args matches id in cookie to show logged-in functionality
#### Check if the user has track iframes, create a list to use in Jinja

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


###OLD README:


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
