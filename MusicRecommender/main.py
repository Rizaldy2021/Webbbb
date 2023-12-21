import streamlit as st
import spotipy
import pickle
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

CLIENT_ID = 'ca7050c731674302a696e8e712724090'
CLIENT_SECRET = 'd4634d69538e4152ab93195180ccb50e'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

data = pd.read_csv('MusicRecommender/visual.csv')

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def song_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    res = sp.search(q=search_query, type="track")
    
    if "tracks" in res and res["tracks"]["items"]:
        track = res["tracks"]["items"][0]
        if "external_urls" in track and "spotify" in track["external_urls"]:
            ex_url = track["external_urls"]["spotify"]
            return ex_url

    return None

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_url = []
    for i in distances[1:11]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append({'song': music.iloc[i[0]].song, 'artist': artist})
        recommended_music_url.append(song_url(music.iloc[i[0]].song, artist))

    return recommended_music_names, recommended_music_posters, recommended_music_url

def generate_wordcloud(text_data):
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text_data)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

tab1, tab2, tab3 = st.tabs(['Recommender', 'Data', 'About'])
with tab1:
    st.header('Music Recommender System')
    
    music = pickle.load(open('MusicRecommender/df.pkl', 'rb'))
    similarity = pickle.load(open('MusicRecommender/similarity.pkl', 'rb'))

    music_list = [f"{song} - {artist}" for song, artist in zip(music['song'], music['artist'])]
    selected_song = st.selectbox(
        "Type or select a song from the dropdown",
        music_list
    )
    fix = selected_song[:selected_song.index(' -')]
    st.write()

    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters, recommended_music_url = recommend(fix)
    
        for i in range(len(recommended_music_names)):
            with st.container():
                column1, column2, column3 = st.columns([0.2, 0.6, 0.2])
                with column1:
                    st.image(recommended_music_posters[i])
                with column2:
                    st.header(recommended_music_names[i]['song'])
                    st.text(recommended_music_names[i]['artist'])
                with column3:
                    if recommended_music_url[i]:    
                        url = recommended_music_url[i]
                        button_key = f"spotify_button_{i}"
                        
                        st.markdown(f"[Spotify]( {url} )", unsafe_allow_html=True)
                    else:
                        st.write("No URL available")
                st.write("")
    
with tab2:
    st.header('Data')
    st.write(data)
    st.write("")
    
    st.header('Word Cloud Visualization')
    
    # Combine all text data into a single string
    text_data = ' '.join(data['text'])  # Replace 'your_text_column_name' with the actual column name containing text data
    
    fig = generate_wordcloud(text_data)
    
    st.pyplot(fig)
    
with tab3:
    st.header('About')
    st.image('MusicRecommender/images1.png', use_column_width='always')
    st.write('Spotify adalah layanan streaming musik digital yang memungkinkan penggunanya mendengarkan jutaan lagu, podcast, dan materi audio lainnya secara online. Dengan model bisnis berlangganan, pengguna dapat membayar biaya bulanan untuk mengakses seluruh katalog musik tanpa iklan, sementara opsi penggunaan gratis menawarkan akses terbatas dengan iklan. Spotify menonjol dengan katalog musiknya yang luas, mencakup berbagai genre dari seluruh dunia. Algoritma personalisasinya menganalisis preferensi mendengar pengguna untuk memberikan rekomendasi yang dipersonalisasi, seperti playlist Discover Weekly. Selain musik, Spotify menawarkan berbagai podcast, mulai dari berita hingga hiburan. Fitur sosial memungkinkan pengguna berbagi lagu dan playlist dengan teman-teman mereka, serta mengikuti aktivitas musik teman. Versi premium menyediakan keuntungan tambahan, termasuk mendengarkan musik tanpa iklan dan kemampuan mengunduh untuk mendengarkan secara offline. Dengan akses lintas platform, pengguna dapat menikmati Spotify di berbagai perangkat, menjadikannya salah satu platform streaming musik paling populer di dunia.')
    st.write('')
    st.write('Music recommender dengan menggunakan cosine similarity adalah sistem yang menggunakan metode perhitungan cosine similarity untuk memberikan rekomendasi musik kepada pengguna berdasarkan kesamaan preferensi mereka. Konsepnya didasarkan pada pengukuran sudut kosinus antara vektor representasi musik yang dibuat berdasarkan preferensi pengguna. Semakin kecil sudut antara vektor, semakin mirip dua set musik tersebut.')
        
