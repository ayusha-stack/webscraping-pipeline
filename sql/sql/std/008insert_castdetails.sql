TRUNCATE TABLE std.cast_members CASCADE;
INSERT INTO std.cast (cast_name)
SELECT DISTINCT unnest(string_to_array(movie_cast, ',')) AS cast_name
FROM std.movies;