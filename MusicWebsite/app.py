import streamlit as st
import os
import sqlite3
import hashlib

# Sayfa Ayarları
st.set_page_config(page_title="Studio Elite v9", page_icon="🎧", layout="wide")

# Klasör ve Veritabanı Yapılandırması
os.makedirs("songs", exist_ok=True)
os.makedirs("covers", exist_ok=True)
conn = sqlite3.connect("underground_v9.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
c.execute(
    "CREATE TABLE IF NOT EXISTS Songs (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, audio_path TEXT, cover_path TEXT, lyrics TEXT)")
conn.commit()

# Oturum Yönetimi
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'expanded_lyrics' not in st.session_state: st.session_state['expanded_lyrics'] = set()


# Şifreleme Fonksiyonları
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()


def check_hashes(p, h): return make_hashes(p) == h


# ==========================================
#      ULTRA ESTETİK CSS (NEON ELITE)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;600;800&display=swap');

    * { font-family: 'Outfit', sans-serif; }
    .stApp { 
        background-color: #050505; 
        background-image: radial-gradient(circle at 50% -20%, #1db95422, transparent);
    }

    /* GİRİŞ KARTLARI */
    .auth-card {
        background: linear-gradient(145deg, #111, #080808);
        padding: 50px;
        border-radius: 40px;
        border: 1px solid #1DB95433;
        box-shadow: 0 20px 60px rgba(0,0,0,1), 0 0 20px rgba(29, 185, 84, 0.1);
        text-align: center;
    }

    /* ŞARKI SATIRI (PREMIUM) */
    .song-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 15px 25px;
        margin-bottom: 12px;
        transition: 0.4s ease;
    }
    .song-item:hover {
        background: rgba(29, 185, 84, 0.06);
        border-color: #1DB954;
        box-shadow: 0 0 30px rgba(29, 185, 84, 0.1);
        transform: translateX(10px);
    }

    /* LYRICS BÖLGESİ */
    .lyrics-view {
        background: #000;
        border-left: 4px solid #1DB954;
        padding: 20px;
        border-radius: 10px;
        color: #888;
        font-size: 0.9rem;
        line-height: 1.7;
        white-space: pre-wrap;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }

    /* KULLANICI ROZETİ */
    .user-tag {
        background: #1DB954;
        color: #000;
        padding: 5px 15px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 0.8rem;
        text-transform: uppercase;
    }

    /* SİLE BUTONU */
    div.stButton > button.delete-btn {
        background: transparent !important;
        border: 1px solid #ff4b4b44 !important;
        color: #ff4b4b !important;
        border-radius: 12px !important;
    }
    div.stButton > button.delete-btn:hover {
        background: #ff4b4b !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- GİRİŞ / KAYIT SİSTEMİ ---
if not st.session_state['logged_in']:
    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#1DB954; letter-spacing:-2px; font-size:3rem;">ELITE STUDIO</h1>',
                    unsafe_allow_html=True)
        st.markdown('<p style="color:#666;">Private Recording Vault Access</p>', unsafe_allow_html=True)

        choice = st.tabs(["🔒 SECURE LOGIN", "✍️ NEW ARTIST"])

        with choice[0]:
            user = st.text_input("Alias", key="login_u")
            pw = st.text_input("Secret", type='password', key="login_p")
            if st.button("OPEN VAULT", use_container_width=True):
                c.execute("SELECT id, password FROM Users WHERE username=?", (user,))
                result = c.fetchone()
                if result and check_hashes(pw, result[1]):
                    st.session_state.update({'logged_in': True, 'user_id': result[0], 'username': user})
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid credentials.")

        with choice[1]:
            new_user = st.text_input("Choose Alias", key="reg_u")
            new_pw = st.text_input("Choose Secret", type='password', key="reg_p")
            if st.button("CREATE ACCOUNT", use_container_width=True):
                if new_user and new_pw:
                    try:
                        c.execute("INSERT INTO Users (username, password) VALUES (?, ?)",
                                  (new_user, make_hashes(new_pw)))
                        conn.commit()
                        st.success("Vault Created. Switch to Login tab.")
                    except:
                        st.error("Alias already taken by another artist.")
                else:
                    st.error("Please fill all fields.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- ANA STÜDYO ARAYÜZÜ ---
with st.sidebar:
    st.markdown(f"### 🎤 <span style='color:#1DB954'>{st.session_state['username']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span class='user-tag'>Authorized Artist</span>", unsafe_allow_html=True)

    if st.button("LOGOUT", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()

    st.markdown("---")
    with st.expander("📀 DROP NEW TRACK", expanded=True):
        audio_file = st.file_uploader("Audio (MP3/WAV)", type=["mp3", "wav"])
        cover_art = st.file_uploader("Cover Art", type=["jpg", "png"])
        lyrics_txt = st.text_area("Lyrics / Bars")

        if st.button("PUSH TO VAULT", use_container_width=True) and audio_file:
            # Dosya İzolasyonu: {user_id}_{filename}
            a_path = os.path.join("songs", f"{st.session_state['user_id']}_{audio_file.name}")
            with open(a_path, "wb") as f:
                f.write(audio_file.getbuffer())

            c_path = ""
            if cover_art:
                c_path = os.path.join("covers", f"{st.session_state['user_id']}_{cover_art.name}")
                with open(c_path, "wb") as f: f.write(cover_art.getbuffer())

            c.execute("INSERT INTO Songs (user_id, name, audio_path, cover_path, lyrics) VALUES (?, ?, ?, ?, ?)",
                      (st.session_state['user_id'], audio_file.name, a_path, c_path, lyrics_txt))
            conn.commit()
            st.rerun()

st.markdown(f'# 🗄️ My <span style="color:#1DB954">Encrypted Vault</span>', unsafe_allow_html=True)
st.markdown(f"<p style='color:#444;'>Artist: {st.session_state['username']}</p>", unsafe_allow_html=True)

# Sadece giriş yapan kullanıcıya ait şarkıları çek
c.execute("SELECT id, name, audio_path, cover_path, lyrics FROM Songs WHERE user_id=? ORDER BY id DESC",
          (st.session_state['user_id'],))
tracks = c.fetchall()

if not tracks:
    st.info("Vault is empty. Use the sidebar to upload your private recordings.")
else:
    # Spotify Header
    h1, h2, h3, h4, h5 = st.columns([0.1, 0.4, 2, 2, 0.2])
    h1.caption("#")
    h2.caption("COVER")
    h3.caption("TRACK DETAILS")
    h4.caption("LISTEN & LYRICS")
    h5.caption("🗑️")

    for i, (tid, name, ap, cp, lyr) in enumerate(tracks):
        st.markdown('<div class="song-item">', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns([0.1, 0.4, 2, 2, 0.2])

        # Sıra No
        c1.markdown(f"<p style='color:#444; margin-top:15px;'>{len(tracks) - i}</p>", unsafe_allow_html=True)

        # Kapak
        with c2:
            if cp and os.path.exists(cp):
                st.image(cp, width=50)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/3002/3002787.png", width=50)

        # İsim ve Sanatçı
        with c3:
            st.markdown(f"<p style='color:#fff; font-weight:600; font-size:1.1rem; margin:0;'>{name}</p>",
                        unsafe_allow_html=True)
            st.markdown(f"<p style='color:#1DB954; font-size:0.8rem; margin:0;'>{st.session_state['username']}</p>",
                        unsafe_allow_html=True)

        # Oynatıcı ve Sözler
        with c4:
            st.audio(ap)
            content = lyr if lyr else "No lyrics recorded for this track."
            lines = content.split('\n')

            # Dinamik Lyrics Genişletme
            if len(lines) > 2 and tid not in st.session_state['expanded_lyrics']:
                st.markdown(f'<div class="lyrics-view">{"/".join(lines[:2])}...</div>', unsafe_allow_html=True)
                if st.button("Read Full Lyrics", key=f"btn_more_{tid}"):
                    st.session_state['expanded_lyrics'].add(tid)
                    st.rerun()
            else:
                st.markdown(f'<div class="lyrics-view">{content}</div>', unsafe_allow_html=True)
                if len(lines) > 2 and st.button("Collapse", key=f"btn_less_{tid}"):
                    st.session_state['expanded_lyrics'].remove(tid)
                    st.rerun()

        # Silme
        with c5:
            if st.button("🗑️", key=f"del_{tid}", type="secondary"):
                c.execute("DELETE FROM Songs WHERE id=?", (tid,))
                conn.commit()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Studio Black Elite Edition v9.0 | Private Artist Isolation Mode")