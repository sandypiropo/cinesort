from flask import Flask, render_template, jsonify, request
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

@app.route('/api/genres')
def get_genres():
    """Get all movie genres plus special LGBT category"""
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured'}), 500
        
        url = f'{TMDB_BASE_URL}/genre/movie/list'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        genres = data.get('genres', [])
        
        # Add special LGBT category
        genres.append({
            'id': 999999,  # Special ID for LGBT
            'name': 'LGBT+'
        })
        
        return jsonify({'genres': genres})
    
    except Exception as e:
        return jsonify({'error': f'Error fetching genres: {str(e)}'}), 500

@app.route('/api/genres-tv')
def get_genres_tv():
    """Get all TV genres plus special LGBT category"""
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured'}), 500
        
        url = f'{TMDB_BASE_URL}/genre/tv/list'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        genres = data.get('genres', [])
        
        # Add special LGBT category
        genres.append({
            'id': 999999,  # Special ID for LGBT
            'name': 'LGBT+'
        })
        
        return jsonify({'genres': genres})
    
    except Exception as e:
        return jsonify({'error': f'Error fetching genres: {str(e)}'}), 500

@app.route('/api/raffle-movie', methods=['GET'])
def raffle_movie():
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured. Set TMDB_API_KEY in .env file'}), 500
        
        genre_id = request.args.get('genre_id')
        random_page = random.randint(1, 500)
        
        url = f'{TMDB_BASE_URL}/discover/movie'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'sort_by': 'popularity.desc',
            'page': random_page,
            'vote_count.gte': 100
        }
        
        # Handle LGBT+ as special case using keywords
        if genre_id == '999999':  # Special ID for LGBT
            params['with_keywords'] = '59967|59969|82295|162564'  # LGBT keywords
        elif genre_id:
            params['with_genres'] = genre_id
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        movies = data.get('results', [])
        
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
        
        # Extract trailer/video
        trailer_url = None
        videos = details.get('videos', {}).get('results', [])
        for video in videos:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                trailer_url = f"https://www.youtube.com/embed/{video['key']}"
                break
        
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
            'cast': [],
            'trailer_url': trailer_url
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

@app.route('/api/raffle-tv', methods=['GET'])
def raffle_tv():
    try:
        if not TMDB_API_KEY:
            return jsonify({'error': 'API key not configured. Set TMDB_API_KEY in .env file'}), 500
        
        genre_id = request.args.get('genre_id')
        random_page = random.randint(1, 500)
        
        url = f'{TMDB_BASE_URL}/discover/tv'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'sort_by': 'popularity.desc',
            'page': random_page,
            'vote_count.gte': 50
        }
        
        # Handle LGBT+ as special case using keywords
        if genre_id == '999999':  # Special ID for LGBT
            params['with_keywords'] = '59967|59969|82295|162564'  # LGBT keywords
        elif genre_id:
            params['with_genres'] = genre_id
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        shows = data.get('results', [])
        
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
        
        # Extract trailer/video
        trailer_url = None
        videos = details.get('videos', {}).get('results', [])
        for video in videos:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                trailer_url = f"https://www.youtube.com/embed/{video['key']}"
                break
        
        # Get episode runtime or use first season info
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
            tv_data['cast'] = [
                actor['name'] for actor in details['credits']['cast'][:5]
            ]
        
        return jsonify(tv_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching TV show: {str(e)}'}), 500
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
