DROP TABLE IF EXISTS raw.movies;
CREATE TABLE IF NOT EXISTS raw.movies (
    movie varchar,
    rating varchar,
    release_year varchar,
    movie_cast VARCHAR
)