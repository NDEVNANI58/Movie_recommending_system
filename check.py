import streamlit as st
import pickle
import requests

movies_list=pickle.load(open('movie_list.pkl','rb'))
movies=movies_list
movies_list=movies_list['title'].values


similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Enter your movie')
selected_movie_name= st.selectbox('Select Movie',movies_list)

def fetch_poster(movie_id):
    url= "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    print(data)
    poster_path=data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommended_movie(movie):
    index=movies[movies['title']== movie].index[0]
    print(movies.head())
    print(similarity[1])
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    # here we are extracting top 5 similar movies
    rec=[]
    rec_posters=[]
    for i in distances[1:5]:
        movie_id=movies.iloc[i[0]].movie_id
        rec_posters.append(fetch_poster(movie_id))
        rec.append(movies.iloc[i[0]].title)
    return rec,rec_posters


if st.button('Recommend'):
    recommendation_movies,recommendation_poster=recommended_movie(selected_movie_name)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(recommendation_movies[0])
        st.image(recommendation_poster[0])
    with col2:
        st.text(recommendation_movies[1])
        st.image(recommendation_poster[1])

    with col3:
        st.text(recommendation_movies[2])
        st.image(recommendation_poster[2])
    with col4:
        st.text(recommendation_movies[3])
        st.image(recommendation_poster[3])

