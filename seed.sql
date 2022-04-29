INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, soundcloud_url, facebook_url, user_type) VALUES ('$2b$12$ThiK5Vj8D9AyXf228cIQPOibIw2VJmpKzQBJxsT6mCkPR5sp29W2S', 'Trambient', 'Sydney', 'blah blah blah', 'sadhorse@example.com', 'danny.jpeg', 'www.dannyatsoundcloud.com', 'http://www.dannyatfb.com','artist');
INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, soundcloud_url, facebook_url, user_type) VALUES ('$2b$12$s0I1uPKvKFBmiYSfa.qao.0vVGu47pCE0iy8vxI1mK6wGlvZsT6ZG', 'N Ticey', 'Sydney', 'blah blah blah', 'enticey@example.com', 'sarah.jpeg', 'www.sarahatsoundcloud.com', 'http://www.sarahatfb.com', 'artist');

INSERT INTO genres (user_id, genre_name) VALUES (1, 'Techno');
INSERT INTO genres (user_id, genre_name) VALUES (1, 'House');
INSERT INTO genres (user_id, genre_name) VALUES (1, 'Disco');
INSERT INTO genres (user_id, genre_name) VALUES (2, 'Disco');

-- INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, soundcloud_url, facebook_url, artist) VALUES ()
-- INSERT INTO users (hashed_password, name, location, bio, email, profile_photo_url, soundcloud_url, facebook_url, artist) VALUES ()


-- INSERT INTO genres (user_id, genre_name) VALUES ('')

-- INSERT INTO genres (genre_name) VALUES ('')
