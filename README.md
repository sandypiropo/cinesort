# CineSort - Movie Raffle Application

A Flask web application that randomly selects movies using the TMDb (The Movie Database) API.

## Features

- Random movie selection from popular movies
- Detailed movie information: poster, backdrop, synopsis, rating, cast, director
- Clean, minimalist dark theme interface
- Responsive design for mobile devices
- Integration with TMDb API

## Prerequisites

- Python 3.8 or higher
- TMDb API key (free account required)

## Installation

1. Clone the repository or navigate to the project folder

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure TMDb API:
   - Visit https://www.themoviedb.org/settings/api
   - Create an account (if you don't have one)
   - Get your API key
   - Copy `.env.example` to `.env`
   - Add your API key to the `.env` file

```bash
copy .env.example .env
```

Edit the `.env` file and replace `your_api_key_here` with your actual API key.

## Running the Application

1. Make sure the virtual environment is activated

2. Run the application:
```bash
python app.py
```

3. Open your browser and visit:
```
http://localhost:5000
```

## How to Use

1. Click the "Raffle Movie" button
2. Wait while the system fetches a random movie
3. View detailed information about the selected movie
4. Click "Raffle Another" to get a different movie
5. Click "View on TMDb" for more information on the official website

## Project Structure

```
cinesort/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example       # Example configuration file
├── .env               # Configuration (do not commit!)
├── templates/
│   └── index.html     # HTML template
└── static/
    └── css/
        └── style.css  # Stylesheets
```

## Technologies Used

- **Flask**: Python web framework
- **TMDb API**: Movie database API
- **HTML/CSS/JavaScript**: Frontend
- **Python Requests**: HTTP client

## License

This project is free for personal and educational use.

## Credits

- Movie data provided by [The Movie Database (TMDb)](https://www.themoviedb.org/)
