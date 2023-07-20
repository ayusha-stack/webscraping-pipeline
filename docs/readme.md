Web Scraping
This repository contains Python utilities and scripts to manage movie data. It includes a PostgreSQL database connection class, a movie data scraper using the OMDB API, and a data management script to store movie details in a PostgreSQL database.

Table of Contents
Prerequisites
Installation
PostgreSQLConnection Class
Movie Data Scraper
Movie Data Management Script
Customization
Error Handling
License
Contact
Prerequisites
Before using the utilities and scripts in this repository, make sure you have the following prerequisites:

Python: Ensure that you have Python installed on your system.
PostgreSQL: Set up a PostgreSQL database and obtain the necessary credentials (host, database name, user, and password).
OMDB API Key: Obtain an API key from OMDB API to access the movie data.
Installation
Clone or download this repository to your local machine.
PostgreSQLConnection Class
The PostgreSQLConnection class allows you to establish a connection to a PostgreSQL database, execute SQL queries, and close the connection.

Usage
Import the class:
python
Copy code
from database.connection import PostgreSQLConnection
Create an instance of PostgreSQLConnection with the appropriate configuration:
python
Copy code
db_connection = PostgreSQLConnection(config_file="database.ini", section="postgresql")
Connect to the database:
python
Copy code
db_connection.connect()
Execute SQL queries:
python
Copy code
sql_query = "SELECT * FROM your_table;"
db_connection.execute_sql(sql_query)
Close the connection when done:
python
Copy code
db_connection.close()
Movie Data Scraper
The "Movie Data Scraper" utility allows you to fetch movie details from the OMDB API, save them to CSV files, and perform data management tasks.

Usage
The utility provides the following functions:

get_movie_details(movie_name, api_key)
This function fetches details of a specific movie using its name and the OMDB API key. It returns a dictionary containing the movie's title, rating, release year, and cast.

python
Copy code
# Example usage:
movie_name = "Inception"
api_key = "your_omdb_api_key"

movie_details = get_movie_details(movie_name, api_key)
if movie_details:
    print(movie_details)
else:
    print("Movie not found or error occurred.")
get_movies_by_genre(movie_genre, api_key)
This function retrieves a list of movies based on their genre using the OMDB API key. It returns a list of movie titles.

python
Copy code
# Example usage:
movie_genre = "action"
api_key = "your_omdb_api_key"

movie_list = get_movies_by_genre(movie_genre, api_key)
print(movie_list)
scrape_movies(movie_list, api_key)
This function fetches movie details for a list of movie names using the OMDB API key. It returns a list of movie details, each represented as a dictionary.

python
Copy code
# Example usage:
movie_list = ["Inception", "The Dark Knight", "Interstellar"]
api_key = "your_omdb_api_key"

movie_details_list = scrape_movies(movie_list, api_key)
print(movie_details_list)
save_movies_to_csv(movie_details_list, filename, directory="data")
This function saves a list of movie details to a CSV file. It creates a "data" directory (if not present) and saves the file in it.

python
Copy code
# Example usage:
movie_details_list = [
    {
        "Movie": "Inception",
        "Rating": "8.8",
        "Release Year": "2010",
        "Cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page"
    },
    {
        "Movie": "The Dark Knight",
        "Rating": "9.0",
        "Release Year": "2008",
        "Cast": "Christian Bale, Heath Ledger, Aaron Eckhart"
    }
]

filename = "movie_details.csv"
save_movies_to_csv(movie_details_list, filename)
Movie Data Management Script
The "Movie Data Management" script provides functionalities to insert CSV data into a PostgreSQL database and execute additional SQL scripts.

Usage
Scrape and Save Movie Details:

Run the script and enter the movie genre when prompted.
The utility will fetch movies for the specified genre using the OMDB API and save their details to a CSV file in the data directory.
Insert CSV Data into PostgreSQL Database:

After generating the CSV files, the utility will insert their data into the specified PostgreSQL database and table.
The CSV data will be inserted into the table using the execute_values method for efficient bulk insertion.
Execute Additional SQL Scripts:

The utility allows you to execute additional SQL scripts located in the sql/sql/std directory.
SQL scripts are executed in alphabetical order, so ensure they have the correct order of execution if interdependent.
Customization
Replace your_host, your_database_name, your_username, your_password, your_table, your_omdb_api_key, and other relevant details specific to your setup.
Modify the column_names list in the insert_csv_files_into_table function to match the columns in your database table.
Update the additional_sql_directory variable in the script to point to the directory containing additional SQL scripts for execution.
