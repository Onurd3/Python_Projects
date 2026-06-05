import streamlit as st
import os
import sqlite3
import hashlib

# ==========================================
# 1. SAYFA AYARLARI & VERİTABANI
# ==========================================
st.set_page_config(page_title="Studio Elite v12.1", page_icon="🎧", layout="wide")

# Klasörleri oluştur
os.makedirs("songs", exist_ok=True)
os.makedirs("covers", exist_ok=True)

# Veritabanı Bağlantısı
conn = sqlite3.connect("underground_v11.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS Songs (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, audio_path TEXT, cover_path TEXT, lyrics TEXT)")
conn.commit()

# --- YARDIMCI FONKSİYONLAR ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h

# ==========================================
# 2. F5 KORUMASI (PERSISTENCE) & SESSION
# ==========================================
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'expanded_lyrics' not in st.session_state: st.session_state['expanded_lyrics'] = set()

# F5 Atıldığında URL'den kullanıcıyı geri çek
if "user" in st.query_params and not st.session_state['logged_in']:
    u_url = st.query_params["user"]
    c.execute("SELECT id FROM Users WHERE username=?", (u_url,))
    res = c.fetchone()
    if res:
        st.session_state.update({'logged_in': True, 'user_id': res[0], 'username': u_url})

# ==========================================
# 3. PREMIUM CSS TASARIMI
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;600;800&display=swap');
    * { font-family: 'Outfit', sans-serif; }
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 2% 10%, #1db95411, transparent 20%); }
    
    /* Login Kutusu */
    .auth-card {
        background: rgba(20, 20, 20, 0.9); padding: 50px; border-radius: 40px;
        border: 1px solid #1DB95433; box-shadow: 0 20px 60px rgba(0,0,0,1); text-align: center;
    }
    
    /* Spotify Satır Stili */
    .song-row {
        background: rgba(255, 255, 255, 0.02); border-radius: 12px;
        padding: 10px 20px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.03);
        transition: 0.3s;
    }
    .song-row:hover { background: rgba(29, 185, 84, 0.05); border-color: #1DB95466; transform: translateX(5px); }

    /* Lyrics Satır Koruması (PRE-WRAP) */
    .lyrics-box {
        background: #000; border-left: 4px solid #1DB954;
        padding: 15px; border-radius: 6px; color: #aaa;
        font-size: 0.9rem; line-height: 1.6; white-space: pre-wrap;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: #222; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #1DB954; }
    
    div.stButton > button { border-radius: 20px; font-weight: 700; transition: 0.2s; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. GİRİŞ & KAYIT EKRANI
# ==========================================
if not st.session_state['logged_in']:
    _, center, _ = st.columns([1, 1.3, 1])
    with center:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#1DB954; margin-bottom:0;">STUDIO ELITE</h1>', unsafe_allow_html=True)
        st.caption("v12.1 - Master Access")
        tab_log, tab_reg = st.tabs(["LOGIN", "REGISTER"])
        
        with tab_log:
            u_in = st.text_input("Username", key="l_u")
            p_in = st.text_input("Password", type='password', key="l_p")
            if st.button("OPEN VAULT", use_container_width=True):
                c.execute("SELECT id, password FROM Users WHERE username=?", (u_in,))
                res = c.fetchone()
                if res and check_hashes(p_in, res[1]):
                    st.session_state.update({'logged_in': True, 'user_id': res[0], 'username': u_in})
                    st.query_params["user"] = u_in 
                    st.rerun()
                else: st.error("Access Refused.")
        
        with tab_reg:
            un = st.text_input("New Artist Name", key="r_u")
            up = st.text_input("New Secret Pass", type='password', key="r_p")
            if st.button("CREATE VAULT", use_container_width=True):
                if un and up:
                    try:
                        c.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (un, make_hashes(up)))
                        conn.commit()
                        st.success("Artist Registered! Please Login.")
                    except: st.error("Alias already taken.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 5. ANA STÜDYO ARAYÜZÜ
# ==========================================
with st.sidebar:
    st.markdown(f"### 🎤 Artist: <span style='color:#1DB954'>{st.session_state['username']}</span>", unsafe_allow_html=True)
    st.caption(f"Artist ID: #{st.session_state['user_id']}")
    
    if st.button("LOGOUT", use_container_width=True):
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()
    
    st.markdown("---")
    with st.expander("📀 DROP NEW TRACK", expanded=True):
        audio_f = st.file_uploader("Audio (MP3/WAV)", type=["mp3", "wav"])
        cover_f = st.file_uploader("Cover Art", type=["jpg", "png"])
        lyrics_f = st.text_area("Write Lyrics Here")
        
        if st.button("PUSH TO VAULT", use_container_width=True) and audio_f:
            a_path = os.path.join("songs", f"u{st.session_state['user_id']}_{audio_f.name}")
            with open(a_path, "wb") as f: f.write(audio_f.getbuffer())
            
            c_path = ""
            if cover_f:
                c_path = os.path.join("covers", f"u{st.session_state['user_id']}_{cover_f.name}")
                with open(c_path, "wb") as f: f.write(cover_f.getbuffer())
            
            c.execute("INSERT INTO Songs (user_id, name, audio_path, cover_path, lyrics) VALUES (?, ?, ?, ?, ?)", 
                      (st.session_state['user_id'], audio_f.name, a_path, c_path, lyrics_f))
            conn.commit()
            st.rerun()

st.markdown(f'# 🗄️ My <span style="color:#1DB954">Encrypted Vault</span>', unsafe_allow_html=True)

c.execute("SELECT id, name, audio_path, cover_path, lyrics FROM Songs WHERE user_id=? ORDER BY id DESC", (st.session_state['user_id'],))
tracks = c.fetchall()

if not tracks:
    st.info("Your vault is empty, artist. Record something to see it here.")
else:
    h_idx, h_img, h_track, h_play, h_del = st.columns([0.2, 0.4, 1.5, 3, 0.2])
    h_idx.caption("#")
    h_img.caption("COVER")
    h_track.caption("TRACK")
    h_play.caption("LISTEN & LYRICS")
    h_del.caption("🗑️")
    st.markdown("<hr style='margin:0; border-color:#222;'>", unsafe_allow_html=True)

    for i, (tid, name, ap, cp, lyr) in enumerate(tracks):
        st.markdown('<div class="song-row">', unsafe_allow_html=True)
        col_idx, col_img, col_track, col_play, col_del = st.columns([0.2, 0.4, 1.5, 3, 0.2])
        
        col_idx.markdown(f"<p style='color:#444; margin-top:15px;'>{len(tracks)-i}</p>", unsafe_allow_html=True)
        
        with col_img:
            if cp and os.path.exists(cp): st.image(cp, width=45)
            else: st.image("https://cdn-icons-png.flaticon.com/512/3002/3002787.png", width=45)
            
        with col_track:
            st.markdown(f"**{name}**")
            st.markdown(f"<span style='color:#1DB954; font-size:0.8rem;'>{st.session_state['username']}</span>", unsafe_allow_html=True)
            
        with col_play:
            if os.path.exists(ap):
                # iOS için format açıkça belirtildi, parça parça akış (stream) destekliyor
                mime_type = "audio/wav" if ap.lower().endswith(".wav") else "audio/mpeg"
                st.audio(ap, format=mime_type)
            else:
                st.error("Audio missing")

            full_lyr = lyr if lyr else "No lyrics recorded."
            lines = full_lyr.split('\n')
            if len(lines) > 2 and tid not in st.session_state['expanded_lyrics']:
                st.markdown(f'<div class="lyrics-box">{"/".join(lines[:2])}...</div>', unsafe_allow_html=True)
                if st.button("Read More", key=f"rm_{tid}"):
                    st.session_state['expanded_lyrics'].add(tid)
                    st.rerun()
            else:
                st.markdown(f'<div class="lyrics-box">{full_lyr}</div>', unsafe_allow_html=True)
                if len(lines) > 2:
                    if st.button("Collapse", key=f"ls_{tid}"):
                        st.session_state['expanded_lyrics'].remove(tid)
                        st.rerun()
        
        with col_del:
            if st.button("🗑️", key=f"del_{tid}"):
                c.execute("DELETE FROM Songs WHERE id=?", (tid,))
                conn.commit()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("⚠️ Disclaimer: This platform is for non-profit, demonstrational purposes only. All rights to the beats belong to their original creators.")
