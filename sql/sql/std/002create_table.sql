DROP TABLE std.movies CASCADE;
CREATE TABLE IF NOT EXISTS  std.movies (
	movie_id serial primary key,
    movie varchar,
    rating FLOAT,
    release_year INT ,
    movie_cast VARCHAR
)

