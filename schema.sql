DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY, 
    hashed_password TEXT NOT NULL,
    name TEXT NOT NULL,
    location TEXT,
    bio TEXT,
    email TEXT,
    profile_photo_url TEXT,
    background_photo_url TEXT,
    soundcloud_url TEXT,
    facebook_url TEXT,
    user_type TEXT
);

CREATE TABLE genres (
    user_id INTEGER REFERENCES users(user_id),
    genre_name TEXT NOT NULL
);

CREATE TABLE tracks (
    user_id INTEGER REFERENCES users(user_id),
    track_url TEXT NOT NULL,
    track_description TEXT,
    track_priority INTEGER
);


-- CREATE TABLE users (
--     user_id SERIAL PRIMARY KEY, 
--     hashed_password TEXT NOT NULL,
--     name TEXT NOT NULL,
--     location TEXT,
--     bio TEXT,
--     email TEXT,
--     profile_photo_url TEXT,
--     soundcloud_url TEXT,
--     facebook_url TEXT,
--     user_type TEXT
-- );

-- CREATE TABLE tracks (
--     user_id INTEGER REFERENCES users(user_id),
--     track_url TEXT NOT NULL,
--     track_priority INTEGER
-- );