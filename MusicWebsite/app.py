import streamlit as st
import os
import sqlite3

# Page Setup
st.set_page_config(page_title="Rap Studio Pro", page_icon="🔥", layout="wide")

# Database & Folders
os.makedirs("songs", exist_ok=True)
os.makedirs("covers", exist_ok=True)
conn = sqlite3.connect("music_v2.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    "CREATE TABLE IF NOT EXISTS Songs (id INTEGER PRIMARY KEY, name TEXT, audio_path TEXT, cover_path TEXT, lyrics TEXT)")
conn.commit()

# Custom CSS for a Premium Look
st.markdown("""
    <style>
    .stApp {background-color: #0E1117; color: #FAFAFA;}
    .track-title {color: #1DB954; font-size: 26px; font-weight: 800; margin-bottom: 5px;}
    .stAudio {width: 100%; margin-top: 10px; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🔥 Underground Rap Studio Pro")

# Sidebar - Upload Section
with st.sidebar:
    st.header("📀 Upload New Record")
    audio_file = st.file_uploader("Audio File (MP3/WAV)", type=["mp3", "wav"])
    cover_file = st.file_uploader("Album Cover (JPG/PNG)", type=["jpg", "png"])
    lyrics_input = st.text_area("Track Lyrics (Optional)", height=150)

    if st.button("➕ Add to Studio", use_container_width=True) and audio_file:
        a_path = os.path.join("songs", audio_file.name)
        with open(a_path, "wb") as f:
            f.write(audio_file.getbuffer())

        c_path = ""
        if cover_file:
            c_path = os.path.join("covers", cover_file.name)
            with open(c_path, "wb") as f: f.write(cover_file.getbuffer())

        c.execute("INSERT INTO Songs (name, audio_path, cover_path, lyrics) VALUES (?, ?, ?, ?)",
                  (audio_file.name, a_path, c_path, lyrics_input))
        conn.commit()
        st.success("Track successfully added!")
        st.rerun()

# Main Area - Playlist & Library
c.execute("SELECT id, name, audio_path, cover_path, lyrics FROM Songs ORDER BY id DESC")
tracks = c.fetchall()

st.metric("Total Tracks in Vault", len(tracks))
st.markdown("---")

if not tracks:
    st.info("The studio is empty. Use the sidebar to upload your first hit!")
else:
    for t_id, name, a_path, c_path, lyrics in tracks:
        with st.container():
            col1, col2 = st.columns([1, 4])

            with col1:
                if c_path and os.path.exists(c_path):
                    st.image(c_path, use_container_width=True)
                else:
                    # Default placeholder image if no cover is uploaded
                    st.image("https://via.placeholder.com/300x300/1A1C23/1DB954?text=No+Cover",
                             use_container_width=True)

            with col2:
                st.markdown(f'<div class="track-title">{name}</div>', unsafe_allow_html=True)
                st.audio(a_path)

                # Expandable Lyrics
                with st.expander("📖 Show Lyrics"):
                    st.write(lyrics if lyrics else "No lyrics provided for this track.")

                # Delete Button
                if st.button(f"🗑️ Delete Track", key=f"del_{t_id}"):
                    c.execute("DELETE FROM Songs WHERE id=?", (t_id,))
                    conn.commit()
                    st.rerun()

            st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("---")
st.caption(
"⚠️ **Disclaimer:** This platform is for non-profit, demonstrational purposes only." +
" The beats used in the tracks do not belong to me;" +
" all rights to the instrumental music belong to their respective original creators.")