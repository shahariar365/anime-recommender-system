import streamlit as st
import pickle
import pandas as pd
import requests
import time 
# --- Page Config ---
st.set_page_config(page_title="AnimeVerse", page_icon="🌌", layout="wide")

# --- Caching Functions ---
@st.cache_resource
def load_data():
    anime_df = pickle.load(open('anime_df.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
    similarity = similarity_matrix.values if isinstance(similarity_matrix, pd.DataFrame) else similarity_matrix
    return anime_df, pt, similarity

# Image caching is CRUCIAL to stop the reloading issue
@st.cache_data(show_spinner=False)
def fetch_poster(anime_id, retries=3):
    for i in range(retries):
        try:
            time.sleep(0.4) 
            response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}')
            
            if response.status_code == 200:
                data = response.json()
                return data['data']['images']['jpg']['large_image_url']
            elif response.status_code == 429:
                time.sleep(2)
        except Exception as e:
            pass
    return "https://placehold.co/225x320/1e1e1e/FFF?text=No+Poster+Found"

@st.cache_data
def get_recommendations(anime_name, _pt, _similarity, _anime_df):
    try:
        index = _pt.index.get_loc(anime_name)
        distances = sorted(list(enumerate(_similarity[index])), reverse=True, key=lambda x: x[1])
        recs = []
        for i in distances[1:6]:
            anime_title = _pt.index[i[0]]
            anime_row = _anime_df[_anime_df['name'] == anime_title].iloc[0]
            recs.append({
                "name": anime_title,
                "poster": fetch_poster(anime_row['anime_id']),
                "rating": f"⭐ {anime_row['rating']:.2f}",
                "members": f"{anime_row['members']:,} Members",
            })
        return recs
    except:
        return []

# Cache the Top 50 HTML. Fixed the Indentation Bug here!
@st.cache_data
def generate_top_50_html(_popular_df):
    html = '<div class="grid-container">'
    for _, row in _popular_df.iterrows():
        poster = fetch_poster(row['anime_id'])
        # No leading spaces to prevent Markdown from treating it as a code block
        html += f'<div class="card"><img src="{poster}" alt="{row["name"]}"><div class="overlay"><h4>{row["name"]}</h4><p>⭐ {row["rating"]:.2f}</p><p>{row["members"]:,} Members</p></div></div>'
    html += '</div>'
    return html

# --- Load Data ---
anime_df, pt, similarity = load_data()

# --- Custom CSS ---
st.markdown("""
<style>
    /* Fix Top Whitespace */
    .block-container {
        padding-top: 1.6rem !important;
        margin-top: 0rem !important;
    }
    
    /* Navbar Style */
    .navbar {
        padding: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #444;
        margin-bottom: 1.5rem;
    }
    .logo { font-size: 1.8rem; font-weight: 800; color: #FF4B4B; letter-spacing: 1px; }
    
    /* Functional Navbar Links */
    .nav-links a { 
        font-size: 1rem; 
        color: #FF4B4B; 
        text-decoration: none; 
        font-weight: bold; 
        margin-left: 20px;
        transition: color 0.3s ease;
    }
    .nav-links a:hover { color: #ffffff; }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.1) 0%, rgba(0, 0, 0, 0.8) 100%), url('https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=2000&auto=format&fit=crop') center/cover;
        padding: 4rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #333;
    }
    .hero h1 { font-size: 3rem; color: white; font-weight: bold; margin-bottom: 0.5rem; }
    .hero p { font-size: 1.1rem; color: #ccc; }

    /* HTML CSS Grid for Top 50 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1.5rem;
    }

    /* Card Styles */
    .card {
        position: relative; border-radius: 8px; overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease; cursor: pointer;
        height: 300px;
    }
    .card:hover { transform: translateY(-8px); box-shadow: 0 10px 20px rgba(255, 75, 75, 0.3); }
    .card img { width: 100%; height: 100%; object-fit: cover; }
    .card .overlay {
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.95) 10%, rgba(0,0,0,0) 70%);
        opacity: 0; transition: opacity 0.3s ease; display: flex;
        flex-direction: column; justify-content: flex-end; padding: 1rem; color: white;
    }
    .card:hover .overlay { opacity: 1; }
    .overlay h4 { margin: 0; font-size: 1rem; font-weight: bold; line-height: 1.2; }
    .overlay p { margin: 0.3rem 0 0 0; font-size: 0.85rem; color: #ddd; }

    /* Footer Style */
    .footer {
        background-color: #0e1117; border-top: 1px solid #333;
        padding: 3rem 1rem; margin-top: 4rem; display: flex; justify-content: space-around; flex-wrap: wrap;
    }
    .footer-col { max-width: 300px; margin-bottom: 1rem; }
    .footer-col h3 { color: #FF4B4B; font-size: 1.2rem; margin-bottom: 1rem; }
    .footer-col p, .footer-col a { color: #888; font-size: 0.9rem; text-decoration: none; display: block; margin-bottom: 0.5rem; }
    .footer-col a:hover { color: white; }
</style>
""", unsafe_allow_html=True)

# --- 1. Navbar ---
st.markdown("""
<div class="navbar">
    <div class="logo">🌌 AnimeVerse</div>
    <div class="nav-links">
        <a href="#search-recommend">Search</a>
        <a href="#top-trending-anime">Top 50</a>
        <a href="#footer">About</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 2. Hero Section ---
st.markdown("""
<div class="hero">
    <h1>Discover Your Next Obsession</h1>
    <p>Explore thousands of anime and get personalized recommendations powered by Machine Learning.</p>
</div>
""", unsafe_allow_html=True)

# --- 3. Search & Recommend Section ---
st.header("🔍 Search & Recommend", anchor="search-recommend")
col_search, col_btn1, col_btn2 = st.columns([6, 2, 2])

with col_search:
    selected_anime = st.selectbox("Search Anime", pt.index, label_visibility="collapsed")

with col_btn1:
    search_clicked = st.button("Recommend Similar", use_container_width=True)

with col_btn2:
    surprise_clicked = st.button("🎲 Surprise Me!", use_container_width=True)

if search_clicked:
    recs = get_recommendations(selected_anime, pt, similarity, anime_df)
    if recs:
        st.markdown("<br><h4>Recommendations for you:</h4>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, rec in enumerate(recs):
            with cols[i]:
                # Fixed indentation here too just in case!
                html_str = f'<div class="card"><img src="{rec["poster"]}" alt="{rec["name"]}"><div class="overlay"><h4>{rec["name"]}</h4><p>{rec["rating"]}</p><p>{rec["members"]}</p></div></div>'
                st.markdown(html_str, unsafe_allow_html=True)
    else:
        st.warning("No recommendations found.")

if surprise_clicked:
    random_anime = anime_df[anime_df['rating'] > 8.0].sample(1).iloc[0]
    st.success(f"🎲 We recommend: **{random_anime['name']}**")
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(fetch_poster(random_anime['anime_id']))
    with col2:
        st.write(f"**Rating:** ⭐ {random_anime['rating']}")
        st.write(f"**Genre:** {random_anime['genre']}")
        st.write(f"**Episodes:** {random_anime['episodes']}")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- 4. Top 50 Section ---
st.header("🏆 Top Trending Anime", anchor="top-trending-anime")
popular_df = anime_df.sort_values('members', ascending=False).head(50)

# Render HTML grid
top_50_html = generate_top_50_html(popular_df)
st.markdown(top_50_html, unsafe_allow_html=True)

# --- 5. Modern Footer ---
st.markdown("""
<div class="footer" id="footer">
    <div class="footer-col">
        <h3>🌌 AnimeVerse</h3>
        <p>Your ultimate destination for discovering anime. Powered by Machine Learning and collaborative filtering.</p>
    </div>
    <div class="footer-col">
        <h3>Quick Links</h3>
        <a href="#top-trending-anime">Trending Now</a>
        <a href="#search-recommend">Find Recommendations</a>
    </div>
    <div class="footer-col">
        <h3>Tech Stack</h3>
        <p>🐍 Python & Pandas</p>
        <p>🎈 Streamlit Framework</p>
        <p>📊 Scikit-Learn</p>
        <p>🔗 Jikan API (MyAnimeList)</p>
    </div>
</div>
""", unsafe_allow_html=True)