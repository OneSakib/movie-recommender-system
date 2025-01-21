import streamlit as st
import pickle
import pandas as pd

MOVIES_DB = "1f4ad2c2d42e329b3598e7fac006f465"
movies_list = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


def fetch_posters(name):
    return f"https://image.tmdb.org./t/p/w500{name}"


def recommanded(movie):
    movie_index = movies_list[movies_list["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list_new = sorted(list(enumerate(distances)),
                             reverse=True, key=lambda x: x[1])[1:6]
    recommanded_movies = []
    for i in movies_list_new:
        movie_id = i[0]
        # Fetch poster
        import requests
        url = f"https://api.themoviedb.org/3/movie/{
            movie_id}?api_key={MOVIES_DB}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        recommanded_movies.append(
            (movies_list.iloc[i[0]].title, fetch_posters(response.json()['poster_path'] if 'poster_path' in response.json() else "")))
    return recommanded_movies


st.title("Movie Recommendation System")
selected_movie_name = st.selectbox(
    "Select Move name to find relevant movie?",
    movies_list['title'].values
)
if st.button("Recommand"):
    recommendations = recommanded(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0][0])
        st.image(recommendations[0][1])
    with col2:
        st.text(recommendations[1][0])
        st.image(recommendations[1][1])
    with col3:
        st.text(recommendations[2][0])
        st.image(recommendations[2][1])
    with col4:
        st.text(recommendations[3][0])
        st.image(recommendations[3][1])
    with col5:
        st.text(recommendations[4][0])
        st.image(recommendations[4][1])
