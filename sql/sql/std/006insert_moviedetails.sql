TRUNCATE TABLE std.movie_details;
INSERT INTO std.movie_details ( movie, rating, release_year)
SELECT
	
    movie, 
    rating,
    release_year
FROM std.movies;