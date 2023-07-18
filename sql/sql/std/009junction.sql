DROP TABLE std.lookup_table;
CREATE TABLE std.lookup_table (
    movie_id INTEGER REFERENCES std.movies(movie_id),
    cast_id INTEGER REFERENCES std.cast(cast_id),
    PRIMARY KEY (movie_id, cast_id)
);