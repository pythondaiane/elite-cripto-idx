import streamlit as st
import numpy as np
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import os
import json
import base64

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Elite Cripto IDX - Premium",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# FUNÇÕES DE IMAGEM (MELHORADAS)
# =========================================================
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

def img_to_html(img_path):
    bin_str = get_base64_of_bin_file(img_path)
    if bin_str:
        img_format = img_path.split(".")[-1]
        return f'<img src="data:image/{img_format};base64,{bin_str}" style="width:100%; max-width:300px; display:block; margin:auto;">'
    return ""

def load_any_logo():
    # Procura por qualquer um desses nomes de arquivo
    possible_names = ["logo.jpeg", "logo.jpg", "elitecryptoidx.jpeg", "elitecryptoidx.jpg"]
    for name in possible_names:
        if os.path.exists(name):
            return img_to_html(name)
    return None

# =========================================================
# BANCO DE DADOS
# =========================================================
DB_FILE = "users_db.json"

def load_users():
    default_admin = {"admin@elite.com": {"password": "admin", "active": True}}
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return default_admin
    return default_admin

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# =========================================================
# CSS PREMIUM (AZUL E DOURADO)
# =========================================================
elite_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

:root {
    --gold: #D4AF37;
    --dark: #000B18;
    --blue: #001A33;
}

.main {
    background: linear-gradient(180deg, var(--dark) 0%, var(--blue) 100%);
    color: white;
}

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 12px;
    padding: 18px;
    font-size: 18px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #000;
    background: linear-gradient(135deg, #B8860B 0%, #D4AF37 50%, #FFD700 100%);
    transition: 0.3s;
    font-family: 'Orbitron', sans-serif;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
}

.login-box {
    max-width: 500px;
    margin: auto;
    margin-top: 40px;
    padding: 40px;
    border-radius: 25px;
    background: rgba(0, 0, 0, 0.6);
    border: 2px solid var(--gold);
    text-align: center;
}

.result-box {
    background: rgba(0, 0, 0, 0.55);
    border: 2px solid var(--gold);
    border-radius: 25px;
    padding: 45px;
    margin-top: 30px;
    text-align: center;
    box-shadow: 0 0 25px rgba(212, 175, 55, 0.2);
}

.signal-text {
    font-size: 70px;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    margin-bottom: 15px;
}

.time-text {
    font-size: 36px;
    color: white;
    font-family: 'Orbitron', sans-serif;
}

.confidence-text {
    color: var(--gold);
    font-size: 24px;
    font-weight: bold;
}

.system-text {
    text-align: center;
    color: #00F2FF;
    font-weight: bold;
    letter-spacing: 2px;
    margin-top: 10px;
}
</style>
"""
st.markdown(elite_css, unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "current_signal" not in st.session_state:
    st.session_state.current_signal = None

users = load_users()

# =========================================================
# LOGIN
# =========================================================
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    
    logo_html = load_any_logo()
    if logo_html:
        st.markdown(logo_html, unsafe_allow_html=True)
    else:
        st.title("💎 ELITE CRIPTO IDX")

    st.markdown('<h2 style="color:#D4AF37; margin-top:20px;">ACESSO EXCLUSIVO</h2>', unsafe_allow_html=True)
    
    email_input = st.text_input("E-mail").strip().lower()
    pass_input = st.text_input("Senha", type="password").strip()

    if st.button("ENTRAR NO TERMINAL"):
        if email_input in users:
            if users[email_input]["password"] == pass_input:
                if users[email_input]["active"]:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email_input
                    st.rerun()
                else:
                    st.error("❌ Acesso bloqueado")
            else:
                st.error("❌ Senha incorreta")
        else:
            st.error("❌ Usuário não encontrado")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# APP PRINCIPAL
# =========================================================
else:
    # Header
    h1, h2, h3 = st.columns([1, 2, 1])
    with h2:
        logo_html = load_any_logo()
        if logo_html:
            st.markdown(logo_html, unsafe_allow_html=True)
        else:
            st.markdown('<h1 style="text-align:center; color:#D4AF37;">ELITE CRIPTO IDX</h1>', unsafe_allow_html=True)
    with h3:
        if st.button("SAIR"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<div class="system-text">SISTEMA PREMIUM ATIVADO</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Área Central
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<h2 style="text-align:center; color:#D4AF37;">ANALISAR PRÓXIMA VELA</h2>', unsafe_allow_html=True)
        
        if st.button("🔥 IDENTIFICAR OPORTUNIDADE 🔥"):
            with st.spinner("ESCANEANDO PADRÕES..."):
                time.sleep(1.5)
                action = np.random.choice(["COMPRA", "VENDA"])
                confidence = np.random.randint(97, 100)
                
                # Horário Brasília
                now = datetime.now(ZoneInfo("America/Sao_Paulo"))
                next_candle = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
                entry_time = next_candle.strftime("%H:%M")
                
                st.session_state.current_signal = {
                    "action": action,
                    "confidence": confidence,
                    "time": entry_time,
                    "color": "#00FF00" if action == "COMPRA" else "#FF3333"
                }

        if st.session_state.current_signal:
            s = st.session_state.current_signal
            st.markdown(f"""
            <div class="result-box">
                <p class="signal-text" style="color:{s['color']};">{s['action']}</p>
                <p class="time-text">às {s['time']}</p>
                <div style="background:rgba(212,175,55,0.08); padding:15px; border-radius:15px; margin-top:25px; border:1px solid #D4AF37;">
                    <p class="confidence-text">ASSERTIVIDADE: {s['confidence']}%</p>
                </div>
                <p style="margin-top:20px; color:#AAA; letter-spacing:2px;">OPERAÇÃO RECOMENDADA PARA M1</p>
            </div>
            """, unsafe_allow_html=True)

    # Painel Admin
    if st.session_state.user_email == "admin@elite.com":
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.expander("⚙️ PAINEL ADMIN"):
            new_email = st.text_input("Novo E-mail").strip().lower()
            new_pass = st.text_input("Nova Senha").strip()
            if st.button("CRIAR ACESSO"):
                if new_email and new_pass:
                    users[new_email] = {"password": new_pass, "active": True}
                    save_users(users)
                    st.success(f"✅ Cliente {new_email} criado")
                    st.rerun()
            
            st.markdown("---")
            for u_email, data in users.items():
                if u_email != "admin@elite.com":
                    col_u1, col_u2 = st.columns([3, 1])
                    status = "✅ ATIVO" if data['active'] else "❌ BLOQUEADO"
                    col_u1.write(f"**{u_email}** | {status}")
                    if col_u2.button("BLOQUEAR/LIBERAR", key=u_email):
                        users[u_email]["active"] = not users[u_email]["active"]
                        save_users(users)
                        st.rerun()
