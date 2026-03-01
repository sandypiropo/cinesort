from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv
import random
import traceback

load_dotenv()

app = Flask(__name__, template_folder="../templates",
            static_folder="../static")

# TMDb API Configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'


@app.route('/')
def index():
    """
    Renders the main application page.
    
    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template('index.html')


@app.route('/api/genres')
def get_genres():
    """
    Fetches available movie genres from TMDb API.
    
    Retrieves all movie genres from TMDB and appends a custom 'LGBT+' genre
    for inclusive content filtering.
    
    Returns:
        dict: JSON object with 'genres' list containing genre id and name.
        tuple: Error response with status code 500 if API key is not configured
               or if request fails.
        
    Raises:
        Exception: Catches and returns any request exceptions as JSON error.
    """
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured'}), 500
    """
    Fetches available TV show genres from TMDb API.
    
    Retrieves all TV show genres from TMDB and appends a custom 'LGBT+' genre
    for inclusive content filtering.
    
    Returns:
        dict: JSON object with 'genres' list containing genre id and name.
        tuple: Error response with status code 500 if API key is not configured
               or if request fails.
        
    Raises:
        Exception: Catches and returns any request exceptions as JSON error.
    """
        url = f'{TMDB_BASE_URL}/genre/movie/list'
        params = {'api_key': TMDB_API_KEY, 'language': 'en-US'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        genres = data.get('genres', [])
        genres.append({'id': 999999, 'name': 'LGBT+'})
        return {'genres': genres}
    except Exception as e:
        return jsonify({'error': f'Error fetching genres: {str(e)}'}), 500


@app.route('/api/genres-tv')
def get_genres_tv():
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured'}), 500
    """
    Performs a random movie raffle with optional genre filtering.
    
    Fetches a random high-rated movie from TMDb, with retry mechanism
    to handle cases where no results are found. Optionally filters by genre.
    Special handling for 'LGBT+' genre (id 999999) using keyword filtering.
    
    Query Parameters:
        genre_id (str, optional): TMDb genre ID or 999999 for LGBT+ content.
                                 Defaults to all genres if not provided.
    
    Returns:
        dict: Movie data including title, synopsis, poster, rating, cast,
              director, release date, runtime, genres, and trailer URL.
        tuple: Error response with status code 404 if no movies found
               or 500 if API key is missing or request fails.
               
    Raises:
        RequestException: Handled and returned as JSON error response.
        Exception: Generic exceptions logged and returned as JSON error.
    """
        url = f'{TMDB_BASE_URL}/genre/tv/list'
        params = {'api_key': TMDB_API_KEY, 'language': 'en-US'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        genres = data.get('genres', [])
        genres.append({'id': 999999, 'name': 'LGBT+'})
        return {'genres': genres}
    except Exception as e:
        return jsonify({'error': f'Error fetching genres: {str(e)}'}), 500


@app.route('/api/raffle-movie', methods=['GET'])
def raffle_movie():
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured. Set TMDB_API_KEY in .env file'}), 500
        genre_id = request.args.get('genre_id')
        max_attempts = 3
        movies = []
        for attempt in range(max_attempts):
            random_page = random.randint(1, 50 if attempt == 0 else 20)
            url = f'{TMDB_BASE_URL}/discover/movie'
            params = {
                'api_key': TMDB_API_KEY,
                'language': 'en-US',
                'sort_by': 'vote_average.desc',
                'page': random_page,
                'vote_count.gte': 50 if attempt > 0 else 100,
                'vote_average.gte': 6.5 if attempt == 0 else 6.0
            }
            if genre_id == '999999':
                params['with_keywords'] = '59967|59969|82295|162564'
            elif genre_id:
                params['with_genres'] = genre_id
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            movies = data.get('results', [])
            if movies:
                break
        if not movies:
            return jsonify({'error': 'No movies found with the selected filters. Try another genre!'}), 404
        movie = random.choice(movies)
        details_url = f'{TMDB_BASE_URL}/movie/{movie["id"]}'
        details_params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'append_to_response': 'credits,videos'
        }
        details_response = requests.get(details_url, params=details_params)
        details_response.raise_for_status()
        details = details_response.json()
        trailer_url = None
        videos = details.get('videos', {}).get('results', [])
        for video in videos:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                trailer_url = f"https://www.youtube.com/embed/{video['key']}"
                break
        movie_data = {
            'id': details['id'],
            'title': details.get('title', 'Title not available'),
    """
    Performs a random TV show raffle with optional genre filtering.
    
    Fetches a random high-rated TV show from TMDb, with retry mechanism
    to handle cases where no results are found. Optionally filters by genre.
    Special handling for 'LGBT+' genre (id 999999) using keyword filtering.
    
    Query Parameters:
        genre_id (str, optional): TMDb genre ID or 999999 for LGBT+ content.
                                 Defaults to all genres if not provided.
    
    Returns:
        dict: TV show data including title, synopsis, poster, rating, cast,
              creator/producer, release date, episode runtime, genres, and
              trailer URL.
        tuple: Error response with status code 404 if no shows found
               or 500 if API key is missing or request fails.
               
    Raises:
        RequestException: Handled and returned as JSON error response.
        Exception: Generic exceptions logged and returned as JSON error.
    """
            'original_title': details.get('original_title', ''),
            'synopsis': details.get('overview', 'Synopsis not available'),
            'poster': f"{TMDB_IMAGE_BASE_URL}{details['poster_path']}" if details.get('poster_path') else None,
            'backdrop': f"https://image.tmdb.org/t/p/original{details['backdrop_path']}" if details.get('backdrop_path') else None,
            'rating': details.get('vote_average', 0),
            'release_date': details.get('release_date', 'Date not available'),
            'genres': [g['name'] for g in details.get('genres', [])],
            'runtime': details.get('runtime', 0),
            'director': None,
            'cast': [],
            'trailer_url': trailer_url
        }
        if 'credits' in details and 'crew' in details['credits']:
            for person in details['credits']['crew']:
                if person['job'] == 'Director':
                    movie_data['director'] = person['name']
                    break
        if 'credits' in details and 'cast' in details['credits']:
            movie_data['cast'] = [actor['name']
                                  for actor in details['credits']['cast'][:5]]
        return movie_data
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching movie: {str(e)}'}), 500
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")

        return jsonify({'error': f'Internal error: {str(e)}'}), 500


if __name__ == "__main__":
    app.run(debug=True)


@app.route('/api/raffle-tv', methods=['GET'])
def raffle_tv():
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured. Set TMDB_API_KEY in .env file'}), 500
        genre_id = request.args.get('genre_id')
        max_attempts = 3
        shows = []
        for attempt in range(max_attempts):
            random_page = random.randint(1, 50 if attempt == 0 else 20)
            url = f'{TMDB_BASE_URL}/discover/tv'
            params = {
                'api_key': TMDB_API_KEY,
                'language': 'en-US',
                'sort_by': 'vote_average.desc',
                'page': random_page,
                'vote_count.gte': 30 if attempt > 0 else 50,
                'vote_average.gte': 6.5 if attempt == 0 else 6.0
            }
            if genre_id == '999999':
                params['with_keywords'] = '59967|59969|82295|162564'
            elif genre_id:
                params['with_genres'] = genre_id
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            shows = data.get('results', [])
            if shows:
                break
        if not shows:
            return jsonify({'error': 'No TV shows found with the selected filters. Try another genre!'}), 404
        show = random.choice(shows)
        details_url = f'{TMDB_BASE_URL}/tv/{show["id"]}'
        details_params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'append_to_response': 'credits,videos'
        }
        details_response = requests.get(details_url, params=details_params)
        details_response.raise_for_status()
        details = details_response.json()
        trailer_url = None
        videos = details.get('videos', {}).get('results', [])
        for video in videos:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                trailer_url = f"https://www.youtube.com/embed/{video['key']}"
                break
        runtime_text = ''
        if details.get('episode_run_time') and len(details['episode_run_time']) > 0:
            runtime_text = f"{details['episode_run_time'][0]}min per episode"
        tv_data = {
            'id': details['id'],
            'title': details.get('name', 'Title not available'),
            'original_title': details.get('original_name', ''),
            'synopsis': details.get('overview', 'Synopsis not available'),
            'poster': f"{TMDB_IMAGE_BASE_URL}{details['poster_path']}" if details.get('poster_path') else None,
            'backdrop': f"https://image.tmdb.org/t/p/original{details['backdrop_path']}" if details.get('backdrop_path') else None,
            'rating': details.get('vote_average', 0),
            'release_date': details.get('first_air_date', 'Date not available'),
            'genres': [g['name'] for g in details.get('genres', [])],
            'runtime': runtime_text,
            'director': None,
            'cast': [],
            'trailer_url': trailer_url
        }
        if 'credits' in details and 'crew' in details['credits']:
            for person in details['credits']['crew']:
                if person['job'] in ['Executive Producer', 'Producer']:
                    tv_data['director'] = person['name']
                    break
        if 'credits' in details and 'cast' in details['credits']:
            tv_data['cast'] = [actor['name']
                               for actor in details['credits']['cast'][:5]]
        return tv_data
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching TV show: {str(e)}'}), 500
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return jsonify({'error': f'Internal error: {str(e)}'}), 500
