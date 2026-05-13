import os
from io import BytesIO
import streamlit as st
import pickle
import requests
from PIL import Image, ImageDraw, ImageFont
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# PAGE CONFIG
st.set_page_config(
    page_title="Hotmass Movies",
    layout="wide",
    page_icon="🎬"
)

# CUSTOM CSS DESIGN
st.markdown("""
<style>

.main {
    background-color: #0f1117;
    color: white;
}

h1, h2, h3, h4 {
    color: white;
}

.stApp {
    background-color: #0f1117;
}

.movie-card {
    background-color: #1c1f26;
    padding: 10px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}

.movie-card:hover {
    transform: scale(1.03);
    box-shadow: 0px 8px 20px rgba(255,0,0,0.4);
}

.movie-title {
    font-size: 18px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

.hero-section {
    background: linear-gradient(to right, #141e30, #243b55);
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
}

.hero-title {
    font-size: 48px;
    font-weight: bold;
    color: white;
}

.hero-subtitle {
    font-size: 20px;
    color: #cccccc;
}

.recommend-box {
    background-color: #1c1f26;
    padding: 25px;
    border-radius: 20px;
    margin-top: 30px;
}

.stButton>button {
    background-color: #e50914;
    color: white;
    border-radius: 10px;
    border: none;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #ff1f1f;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🎬 Hotmass Movies</div>
    <div class="hero-subtitle">
        Discover Trending Movies & Get Smart Recommendations
    </div>
</div>
""", unsafe_allow_html=True)


# TOP MOVIES SECTION
st.subheader("🔥 Top 5 Mostly Watched Movies")

movie_names = [
    "The Dark Knight",
    "Inception",
    "Interstellar",
    "Avengers: Endgame",
    "Avatar"
]

movie_posters = [
    "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
    "https://image.tmdb.org/t/p/w500/kyeqWdyUXW608qlYkRqosgbbJyK.jpg"
]

cols = st.columns(5)

for i in range(5):

    with cols[i % 5]:

        st.markdown('<div class="movie-card">', unsafe_allow_html=True)

        st.image(movie_posters[i], width=200)

        st.markdown(
            f'<div class="movie-title">{movie_names[i]}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

# LOAD DATA
import pandas as pd

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "moviedataset.csv")

movie_data = pd.read_csv(csv_path)

# Compute similarity matrix from genres
try:
    tfidf = TfidfVectorizer(analyzer='char', ngram_range=(2, 2))
    genre_vectors = tfidf.fit_transform(movie_data["genre"].fillna(""))
    similarity = cosine_similarity(genre_vectors)
except Exception as e:
    st.error(f"❌ Error computing similarity: {str(e)}")
    st.stop()

# TMDB API KEY - Use environment variable for security
api_key = os.getenv("TMDB_API_KEY", "72d6eb78b2ce09c9ee018faaf3e54782")

# RECOMMENDATION SECTION
st.markdown("""
<div class="recommend-box">
""", unsafe_allow_html=True)

st.subheader("🎯 Find Movie Suggestions")

movie_list = movie_data["title"].values

selected_movie = st.selectbox(
    "Search or Select a Movie",
    movie_list
)

# PLACEHOLDER IMAGE
def create_placeholder_image(text="No Image"):

    width, height = 500, 750

    image = Image.new("RGB", (width, height), color=(20, 20, 20))

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except Exception:
        font = ImageFont.load_default()

    try:
        text_width, text_height = draw.textsize(text, font=font)
    except Exception:
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except Exception:
            text_width, text_height = font.getsize(text)

    draw.text(
        ((width - text_width) / 2, (height - text_height) / 2),
        text,
        font=font,
        fill=(255, 255, 255),
    )

    buffer = BytesIO()

    image.save(buffer, format="PNG")

    buffer.seek(0)

    return buffer.read()

# FETCH POSTER FUNCTION
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

    except Exception:

        return create_placeholder_image("API Error")

    poster_path = data.get("poster_path")

    if not poster_path:

        return create_placeholder_image("No Poster")

    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"

    try:

        image_response = requests.get(full_path, timeout=10)

        image_response.raise_for_status()

        return image_response.content

    except Exception:

        return create_placeholder_image("Image Error")

# RECOMMEND FUNCTION
def recommend(movie):
    try:
        movie_index = movie_data[movie_data["title"] == movie].index
        
        if len(movie_index) == 0:
            st.error(f"Movie '{movie}' not found in dataset")
            return [], []
        
        movie_index = movie_index[0]
        selected_vector = genre_vectors[movie_index]
        similarity_scores = cosine_similarity(selected_vector, genre_vectors)[0]

        distance = sorted(
            list(enumerate(similarity_scores)),
            reverse=True,
            key=lambda x: x[1]
        )

        recommended_movies = []
        recommended_movies_posters = []

        # 10 RECOMMENDATIONS
        for i in distance[1:11]:
            movie_id = movie_data.iloc[i[0]].id
            recommended_movies.append(movie_data.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_movies_posters
    except Exception as e:
        st.error(f"Error in recommend function: {str(e)}")
        import traceback
        st.write(traceback.format_exc())
        return [], []

# RECOMMEND BUTTON
if st.button("🎥 Your Next Movie"):
    try:
        recommended_movies, recommended_movies_posters = recommend(selected_movie)

        st.subheader("✨ Recommended For You")

        cols = st.columns(5)

        if not recommended_movies:
            st.warning("No recommendations were generated. Please try another movie.")
        else:
            for i in range(len(recommended_movies)):
                with cols[i % 5]:
                    st.markdown(
                        '<div class="movie-card">',
                        unsafe_allow_html=True
                    )

                    st.image(
                        recommended_movies_posters[i],
                        width=200
                    )

                    st.markdown(
                        f'<div class="movie-title">{recommended_movies[i]}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )
    except Exception as e:
        st.error(f"❌ Error generating recommendations: {str(e)}")
        st.info(f"Selected movie: {selected_movie}")
        import traceback
        st.write(traceback.format_exc())
    except Exception as e:
        st.error(f"❌ Error generating recommendations: {str(e)}")
        st.info(f"Selected movie: {selected_movie}")
        import traceback
        st.write(traceback.format_exc())

st.markdown("</div>", unsafe_allow_html=True)

## footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #555555;">
    <p>© 2026 Hotmass Movies. All rights reserved.</p>
    <p>Built with Streamlit & TMDB API</p>
</div>
""", unsafe_allow_html=True)
