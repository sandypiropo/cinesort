from flask import Flask, render_template, jsonify
import requests
import os
from dotenv import load_dotenv
import random
import traceback

load_dotenv()

app = Flask(__name__)

# TMDb API Configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/raffle-movie')
def raffle_movie():
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured. Set TMDB_API_KEY in .env file'}), 500
        
        random_page = random.randint(1, 500)
        
        url = f'{TMDB_BASE_URL}/discover/movie'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'sort_by': 'popularity.desc',
            'page': random_page,
            'vote_count.gte': 100
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        movies = data.get('results', [])
        
        if not movies:
            return jsonify({'error': 'No movies found'}), 404
        
        movie = random.choice(movies)
        
        details_url = f'{TMDB_BASE_URL}/movie/{movie["id"]}'
        details_params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'append_to_response': 'credits'
        }
        
        details_response = requests.get(details_url, params=details_params)
        details_response.raise_for_status()
        details = details_response.json()
        
        movie_data = {
            'id': details['id'],
            'title': details.get('title', 'Title not available'),
            'original_title': details.get('original_title', ''),
            'synopsis': details.get('overview', 'Synopsis not available'),
            'poster': f"{TMDB_IMAGE_BASE_URL}{details['poster_path']}" if details.get('poster_path') else None,
            'backdrop': f"https://image.tmdb.org/t/p/original{details['backdrop_path']}" if details.get('backdrop_path') else None,
            'rating': details.get('vote_average', 0),
            'release_date': details.get('release_date', 'Date not available'),
            'genres': [g['name'] for g in details.get('genres', [])],
            'runtime': details.get('runtime', 0),
            'director': None,
            'cast': []
        }
        
        if 'credits' in details and 'crew' in details['credits']:
            for person in details['credits']['crew']:
                if person['job'] == 'Director':
                    movie_data['director'] = person['name']
                    break
        
        if 'credits' in details and 'cast' in details['credits']:
            movie_data['cast'] = [
                actor['name'] for actor in details['credits']['cast'][:5]
            ]
        
        return jsonify(movie_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching movie: {str(e)}'}), 500
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
