import os
import pandas as pd
from DATABASE.connection import PostgreSQLConnection
from psycopg2.extras import execute_values
from scrape.scrape import get_movies_by_genre, scrape_movies, save_movies_to_csv

# Function to execute an SQL file using the PostgreSQLConnection class
def execute_sql_file(sql_file, db_connection):
    script_path = os.path.join(os.path.dirname(__file__), sql_file)

    with open(script_path, 'r') as file:
        sql_script = file.read()

    try:
        cursor = db_connection.connection.cursor()
        cursor.execute(sql_script)
        db_connection.connection.commit()
        print(f"Executed SQL file: {sql_file}")
    except Exception as e:
        print(f"Error executing SQL file '{sql_file}':", e)

# Function to insert CSV data into the PostgreSQL database table
def insert_csv_files_into_table(directory, schema, table_name):
    csv_files = [file for file in os.listdir(directory) if file.endswith(".csv")]
    if not csv_files:
        print("No CSV files found in the directory.")
        return

    # Create an instance of PostgreSQLConnection
    db_connection = PostgreSQLConnection()

    # Connect to the database
    db_connection.connect()

    try:
        # Execute the SQL files in order
        execute_sql_file("sql/sql/raw/create_schema.sql", db_connection)
        execute_sql_file("sql/sql/raw/create_table.sql", db_connection)

        for csv_file in csv_files:
            try:
                csv_path = os.path.join(directory, csv_file)
                # Define the column names to ensure consistency
                column_names = ["movie", "rating", "release_year", "movie_cast"]
                # Read the CSV file into a DataFrame, specifying the column names and skipping the header row
                df = pd.read_csv(csv_path, names=column_names, skiprows=1)

                # Convert the 'movie_cast' column to strings and then split by comma to get the cast list
                df['movie_cast'] = df['movie_cast'].apply(lambda x: [cast.strip() for cast in x.split(",")])

                # Prepare the data for insertion as a list of tuples
                data = [tuple(row) for _, row in df.iterrows()]

                # Define the SQL query to insert data into the table
                insert_data_query = f"INSERT INTO {schema}.{table_name} (movie, rating, release_year, movie_cast) VALUES %s;"

                # Execute the SQL query to insert data into the table using execute_values
                execute_values(db_connection.connection.cursor(), insert_data_query, data)

                # Commit the changes after each CSV file insertion
                db_connection.connection.commit()

                print(f"{len(df)} rows inserted successfully from '{csv_file}' to '{schema}.{table_name}'.")
            except Exception as e:
                print(f"Error inserting data from '{csv_file}':", e)
                # Rollback the transaction in case of an error
                db_connection.connection.rollback()

    except Exception as e:
        print("Error executing SQL files:", e)
    finally:
        # Close the connection
        db_connection.close()
def execute_additional_sql_files(sql_directory, db_connection):
    sql_files = [file for file in os.listdir(sql_directory) if file.endswith(".sql")]
    if not sql_files:
        print("No SQL files found in the directory.")
        return

    # Sort the SQL files based on their filenames
    sql_files.sort()
    print(sql_files.sort())

    try:
        for sql_file in sql_files:
            try:
                sql_file_path = os.path.join(sql_directory, sql_file)
                execute_sql_file(sql_file_path, db_connection)
            except Exception as e:
                print(f"Error executing SQL file '{sql_file_path}':", e)
                # Rollback the transaction in case of an error
                db_connection.connection.rollback()

    except Exception as e:
        print("Error executing SQL files:", e)


# Example usage:
if __name__ == "__main__":
    # Directory containing CSV files
    directory_path = "data"

    # Schema and table name
    schema_name = "raw"  # Replace with your actual schema name
    table_name = "movies"

    # Replace "YOUR_OMDB_API_KEY" with the API key you obtained from the OMDB website.
    omdb_api_key = "2e768c90"

    # Prompt the user to enter the movie genre
    movie_genre = input("Enter the movie genre: ")

    # Get movies by genre using OMDB API
    movie_list = get_movies_by_genre(movie_genre, omdb_api_key)

    if movie_list:
        # Scrape and save movie details to a CSV file
        movie_details_list = scrape_movies(movie_list, omdb_api_key)
        if movie_details_list:
            filename = f"{movie_genre}_movies.csv"
            save_movies_to_csv(movie_details_list, filename)
            print(f"Movie details for '{movie_genre}' genre saved to 'data/{filename}'.")
        else:
            print(f"No movie details found for '{movie_genre}' genre.")
    else:
        print(f"No movies found for '{movie_genre}' genre in the OMDB database.")

    # Insert CSV data into the table after CSV files are generated
    insert_csv_files_into_table(directory_path, schema_name, table_name)
    additional_sql_directory = "sql/sql/std"

    # Create an instance of PostgreSQLConnection
    db_connection = PostgreSQLConnection()

    # Connect to the database
    db_connection.connect()

    # Execute additional SQL files
    execute_additional_sql_files(additional_sql_directory, db_connection)

    # Close the connection
    db_connection.close()