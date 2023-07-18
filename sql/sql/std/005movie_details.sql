DROP TABLE  IF EXISTS std.movie_details CASCADE;
CREATE TABLE IF NOT EXISTS std.movie_details (
    movie_id SERIAL PRIMARY KEY,
    movie VARCHAR NOT NULL,
    rating FLOAT,
    release_year INT
);