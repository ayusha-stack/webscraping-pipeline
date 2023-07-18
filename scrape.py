import requests
import os

def get_movie_details(movie_name, api_key):
    # OMDB API endpoint
    omdb_url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name}"

    try:
        # Send a request to OMDB API
        response = requests.get(omdb_url)
        data = response.json()

        # Check if the movie was found in the database
        if data.get("Response") == "True":
            movie_title = data["Title"]
            movie_cast = data["Actors"]
            movie_rating = data["imdbRating"]
            movie_release_year = data["Year"]

            # Return the movie details as a dictionary
            return {
                "Movie": movie_title,
                "Rating": movie_rating,
                "Release Year": movie_release_year,
                "Cast": movie_cast
            }
        else:
            return None

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None

def get_movies_by_genre(movie_genre, api_key):
    # OMDB API endpoint
    omdb_url = f"http://www.omdbapi.com/?apikey={api_key}&s={movie_genre}&type=movie"

    try:
        # Send a request to OMDB API to get a list of movies by genre
        response = requests.get(omdb_url)
        data = response.json()

        if data.get("Response") == "True":
            movies = data.get("Search", [])

            # Return a list of movie titles
            return [movie["Title"] for movie in movies]

        return []

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return []

def scrape_movies(movie_list, api_key):
    movie_details_list = []

    for movie_name in movie_list:
        # Fetch movie details using the OMDB API
        movie_details = get_movie_details(movie_name, api_key)
        if movie_details:
            movie_details_list.append(movie_details)

    return movie_details_list

def save_movies_to_csv(movie_details_list, filename, directory="data"):
    # Create the "data" directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Append the directory path to the filename
    filepath = os.path.join(directory, filename)

    import csv
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=movie_details_list[0].keys())
        writer.writeheader()
        writer.writerows(movie_details_list)
