import streamlit as st
import pickle
import pandas as pd
import requests

ich_bin_ashutosh = 'https://github.com/ashitoshn3598'

st.markdown(ich_bin_ashutosh, unsafe_allow_html=True)

api_key = 'cc74e26a0429e1c3332cbb3c55e36f12'
def get_image(id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US')
    data = response.json()
    print(data)
    return 'https://image.tmdb.org/t/p/original/'+ data['poster_path']

def recommonder(movie,n):
    index = movies_n[movies_n.title == movie].index[0]
    cos_sim = similarity[index]
    index_ls = sorted(list(enumerate(cos_sim)),reverse=True,key=lambda x:x[1])[1:n+1]

    rec_mov = []
    images = []
    for i in index_ls:
        rec_mov.append(movies_n.iloc[i[0]].title)
        images.append(get_image(movies_n.iloc[i[0]].id))
    return rec_mov,images

movies_n = pickle.load(open('movies.pkl','rb'))
movies_list = movies_n.title.values

similarity = pickle.load(open('sim.pkl','rb'))

st.title("Movie recommendation System")

option = st.selectbox('Search Movies Here',movies_list)
no_of_movies = st.selectbox('No. of movies',list(range(1,100)))

def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

mygrid = make_grid(no_of_movies//4+1,4)

if st.button('Recommend'):
    name,image = recommonder(option,no_of_movies)
    count = 0
    n = no_of_movies
    m = 0
    for i in range(n//4+n%4):
        for j in range(4):
            mygrid[i][j].write(name[m])
            mygrid[i][j].image(image[m])
            count= count+1
            m=m+1
            if count ==n: 
                break
        if count ==n: 
            break