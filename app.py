import pickle
import streamlit as st
import requests
import os
import gdown

# ---------------------- STREAMLIT UI ----------------------

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender System")

# ---------------------- DOWNLOAD MODEL IF NOT EXISTS ----------------------

MODEL_PATH = "model/similarity.pkl"

if not os.path.exists(MODEL_PATH):
    with st.spinner("Downloading similarity model... Please wait ⏳"):
        url = "https://drive.google.com/uc?id=1x8WScNQ36KccDJUSRX6x8rDo21xu4QFZ"
        gdown.download(url, MODEL_PATH, quiet=False)

# ---------------------- LOAD DATA ----------------------

movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open(MODEL_PATH, 'rb'))

# ---------------------- FETCH POSTER ----------------------

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f7deea27bc8cd3f40981737249ef57ba&language=en-US"

        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

        return "https://via.placeholder.com/300x450?text=No+Image"

    except:
        return "https://via.placeholder.com/300x450?text=Error"

# ---------------------- RECOMMEND FUNCTION ----------------------

def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# ---------------------- UI ----------------------

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):

    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])