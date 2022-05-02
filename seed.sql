INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, background_photo_url, soundcloud_url, facebook_url, user_type) VALUES ('$2b$12$ThiK5Vj8D9AyXf228cIQPOibIw2VJmpKzQBJxsT6mCkPR5sp29W2S', 'Trambient', 'Sydney', 'Just a couple of guys making some noises', 'trambient@example.com', 'https://cdn.pixabay.com/photo/2014/04
/03/11/51/tram-312371_1280.png', 'https://cdn.pixabay.com/photo/2022/01/02/19/43/train-6910973_1280.jpg', 'https://soundcloud.com/suzuki-growhouse', 'http://www.dannyatfb.com','artist');

INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, background_photo_url, soundcloud_url, facebook_url, user_type) VALUES ('$2b$12$s0I1uPKvKFBmiYSfa.qao.0vVGu47pCE0iy8vxI1mK6wGlvZsT6ZG', 'Sadhorse', 'Melbourne', 'Entertainment not guaranteed', 'sadhorse@example.com', 'https://i1.sndcdn.com/avatars-7NOAQlX5rE0P1NUK-tvht1Q-t500x500.jpg', 'https://i1.sndcdn.com/visuals-000038796715-PYDux3-t2480x520.jpg', 'https://soundcloud.com/suzuki-growhouse', 'http://www.sadhorseatfb.com', 'artist');

INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, background_photo_url, soundcloud_url, facebook_url, user_type) VALUES ('$2b$12$s0I1uPKvKFBmiYSfa.qao.0vVGu47pCE0iy8vxI1mK6wGlvZsT6ZG', 'N Ticey', 'Sydney', 'blah blah blah', 'enticey@example.com', 'https://i.ebayimg.com/images/g/ydcAAOSwqvlg4nhT/s-l400.jpg', 'https://i1.sndcdn.com/visuals-000012858223-wA55yg-t2480x520.jpg', 'https://soundcloud.com/monolink', 'http://www.sarahatfb.com', 'artist');

INSERT INTO genres (user_id, genre_name) VALUES (1, 'Techno');
INSERT INTO genres (user_id, genre_name) VALUES (1, 'House');
INSERT INTO genres (user_id, genre_name) VALUES (1, 'Disco');
INSERT INTO genres (user_id, genre_name) VALUES (2, 'Techno');
INSERT INTO genres (user_id, genre_name) VALUES (2, 'House');
INSERT INTO genres (user_id, genre_name) VALUES (2, 'Disco');
INSERT INTO genres (user_id, genre_name) VALUES (3, 'Disco');
INSERT INTO genres (user_id, genre_name) VALUES (3, 'Techno');

INSERT INTO tracks (user_id, track_url, track_description, track_priority) VALUES (1, 'https://soundcloud.com/suzuki-growhouse/smol-attack', 'Just a couple bros making some noises', 1);

INSERT INTO tracks (user_id, track_url, track_description, track_priority) VALUES (2, 'https://soundcloud.com/suzuki-growhouse/lcd-warhols', 'A fun time for the whole family', 1);

INSERT INTO tracks (user_id, track_url, track_description, track_priority) VALUES (3, 'https://soundcloud.com/barchef-1/monolink-live-from-his-berlin-studio', 'Just vibes', 1);




-- INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, soundcloud_url, facebook_url, artist) VALUES ()
-- INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, soundcloud_url, facebook_url, artist) VALUES ()

-- url(https://i1.sndcdn.com/visuals-000012858223-wA55yg-t2480x520.jpg)

-- INSERT INTO genres (user_id, genre_name) VALUES ('')

-- INSERT INTO genres (genre_name) VALUES ('')

-- INSERT INTO tracks (user_id, track_url, track_description, 1) VALUES (2, '', '');