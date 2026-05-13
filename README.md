# Recommended Movie System

## Overview

This project is a movie recommendation app built with Streamlit and Python. It loads a movie dataset, computes similarity scores based on movie genres, and provides movie recommendations through a web interface. The app also displays a set of popular movie posters and allows users to select a movie to receive 10 recommended movies.

## Project Structure

- `movie.py` - Main Streamlit application file.
- `movie_rec.ipynb` - Jupyter notebook containing exploratory data analysis, feature extraction, and recommendation system logic.
- `moviedataset.csv` - Movie dataset used by the app.
- `requirements.txt` - Python package dependencies required to run the app.
- `runtime.txt` - Specifies the Python runtime version for deployment platforms like Render.
- `.gitignore` - Files and folders excluded from Git.
- `posters/` - Local folder for poster images (downloaded during notebook execution or app testing).

## How It Works

1. **Data Loading**
   - The app reads `moviedataset.csv` to load movie titles, genres, and other metadata.

2. **Similarity Calculation**
   - It uses `TfidfVectorizer` from `scikit-learn` to transform movie genres into numerical vectors.
   - The app computes cosine similarity between these vectors to determine how similar movies are to each other.

3. **User Interface**
   - Streamlit renders a modern web UI with a hero section and top movie cards.
   - Users can select a movie from a dropdown list.
   - When the user clicks the recommendation button, the app returns 10 similar movies.

4. **Poster Display**
   - Poster images are displayed using a responsive helper function to ensure they fit mobile screens.
   - The app fetches poster images from TMDB via the movie ID when recommending movies.

## Setup Instructions

### Requirements

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### Run Locally

Launch the Streamlit app from the project directory:

```bash
streamlit run movie.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

## Deployment

This app is configured for deployment on services like Render.

### Render Setup

- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run movie.py --server.port $PORT --server.headless true`
- Runtime version: `python-3.11.9` (specified in `runtime.txt`)

### Notes

- `tensorflow` was intentionally removed from `requirements.txt` to ensure compatibility with Render, since the deployed app does not require TensorFlow for generation of recommendations.
- The app uses a lightweight genre-based recommendation approach, so it installs quickly and runs efficiently.

## Development Notes

- If you want to expand recommendations, you can improve the dataset or add more features such as movie overviews, cast, crew, or poster image embeddings.
- The current app returns 10 recommendations and supports responsive image rendering for mobile devices.

## Version Control

This repository is hosted at:

- `https://github.com/thomasgodfrey448-netizen/Recommended-Movie-system`

## Author

- Project by Thomas Godfrey

---

Enjoy exploring movies and getting smart recommendations with this Streamlit-powered system!
