TRUNCATE TABLE std.movies;

INSERT INTO std.movies (movie, rating, release_year, movie_cast)
SELECT
    movie,
    rating::float,
    release_year::int,
    REPLACE(REPLACE(REPLACE(movie_cast, '{', ''), '}', ''), '"', '') AS actor_names
FROM
    raw.movies;
SELECT * FROM std.movies;