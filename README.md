# 🌌 AnimeVerse - Machine Learning Recommendation System

![AnimeVerse Dashboard](banner.png)
<img width="1912" height="876" alt="image" src="https://github.com/user-attachments/assets/ce887781-56b8-4f17-bf8e-90d649cf469d" />

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://anime-verse.streamlit.app/) 
*(Click the badge above to view the live application!)*


## 📌 Overview
**AnimeVerse** is an advanced, Machine Learning-powered Anime Recommendation Engine. It goes beyond simple genre-matching and utilizes human psychology and viewing behaviors to suggest anime. Whether you are looking for hidden gems similar to your favorites, or want to explore the top trending shows globally, AnimeVerse is your gateway to infinite anime.

## ✨ Key Features
* **🧠 Smart Recommendations:** Uses Item-Based Collaborative Filtering to recommend anime based on collective user behavior.
* **🎲 Surprise Me:** A randomized generator that picks a highly-rated anime (Score > 8.0) for when you can't decide what to watch.
* **🏆 Top 50 Trending:** A dynamically generated grid of the top 50 most popular anime in the world.
* **🎨 Modern UI/UX:** Built with Streamlit but heavily customized with CSS to provide a premium streaming-site experience (like Crunchyroll/Netflix) featuring hover-overlay cards.
* **⚡ Blazing Fast:** Utilizes `@st.cache_data` to minimize API calls and prevent page reloads, ensuring a seamless user experience.

---

## ⚙️ How the Recommendation Engine Works

AnimeVerse does **NOT** recommend anime by looking at its genre, synopsis, or studio (Content-Based). Instead, it uses **Item-Based Collaborative Filtering**. 

**The Math Behind the Magic (Cosine Similarity):**
1. We created a massive **Vector Space (Pivot Table)** where rows are Anime, columns are Users, and the values are the Ratings (1-10) given by the users.
2. If a user searches for an anime (e.g., *"Death Note"*), the algorithm looks at the vector of *Death Note*.
3. It then calculates the distance between the *Death Note* vector and all other anime vectors using **Cosine Similarity**.
4. The mathematical formula finds hidden patterns. For example, it notices that users who highly rate *Death Note* also tend to highly rate *Code Geass* and *Attack on Titan*.
5. The system sorts these similarity scores and returns the top 5 closest matches. 

*Result: You get recommendations based on actual human viewing habits, not just tags!*

---

## 💻 Code Architecture & Explanation

The project is divided into two main phases: Data Modeling and Frontend Development.

### Phase 1: Data Preprocessing & ML Modeling (`Jupyter Notebook`)
* **Data Cleaning:** Loaded Kaggle datasets (`anime.csv`, `rating.csv`). Unescaped HTML characters (e.g., converting `&quot;` to `"`).
* **Noise Reduction:** Filtered out inactive users (who rated less than 250 anime) and unpopular anime (rated by less than 100 users). This strict filtering reduced memory usage and increased the accuracy of the model.
* **Model Building:** Created a Pivot Table and applied `sklearn.metrics.pairwise.cosine_similarity`. 
* **Export:** Serialized the DataFrames and similarity matrix using `pickle` (`.pkl` files) to act as the brain for the web app. *(Note: Data types were downcasted to `float32` and `float16` to reduce the file size from 1.2GB to under 50MB for GitHub deployment).*
* This is actually Item-Based Collaborative Filtering, which is also used by Netfilx and Amazon.

### Phase 2: Web App Development (`app.py`)
* **Framework:** Used **Streamlit** for rapid UI development.
* **API Integration:** Integrated the **Jikan API (Unofficial MyAnimeList API)** to fetch high-quality anime posters in real-time. 
* **Rate Limiting Handling:** Engineered a retry mechanism with `time.sleep()` to prevent API blocking (Error 429: Too Many Requests) while fetching 50 posters at once.
* **Caching:** Implemented Streamlit caching (`@st.cache_resource` and `@st.cache_data`) to store API responses and ML calculations in memory, making the app lightning-fast after the initial load.
* **Custom Styling:** Injected custom HTML & CSS to override Streamlit's default UI, adding a gradient hero section, a sticky navbar, and interactive hover-cards.

---

## 🛠️ Tech Stack
* **Language:** Python 3
* **Data Manipulation:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn
* **Web Framework:** Streamlit
* **API:** RESTful API (Requests library) interacting with Jikan API
* **Deployment:** Streamlit Community Cloud

---

## 🚀 Run it Locally

To run this project on your local machine:

1. Clone the repository:
```bash
git clone https://github.com/shahariar365/anime-recommender-system.git
cd anime-recommender-system
