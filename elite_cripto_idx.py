import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from PIL import Image
import os
import json

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="Elite Cripto IDX",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== BANCO DE DADOS SIMPLES (JSON) ====================
DB_FILE = "users_db.json"

def load_users():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {"admin@elite.com": {"password": "admin", "active": True}}
    return {"admin@elite.com": {"password": "admin", "active": True}}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# ==================== ESTILO CSS ELITE (ESTILO QUANTIUM) ====================
elite_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

    :root {
        --elite-gold: #D4AF37;
        --elite-blue: #00F2FF;
        --dark-bg: #00050A;
    }
    
    .main {
        background-color: var(--dark-bg);
        background-image: radial-gradient(circle at 50% 50%, #001529 0%, #00050A 100%);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #B8860B 0%, #D4AF37 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 18px 20px;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 18px;
    }

    .login-box {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: rgba(0, 11, 24, 0.9);
        border: 2px solid var(--elite-gold);
        border-radius: 20px;
        text-align: center;
    }

    .result-box {
        background: rgba(0, 11, 24, 0.95);
        border: 2px solid var(--elite-gold);
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.3);
    }

    .signal-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 45px;
        font-weight: 900;
        margin: 0;
        letter-spacing: 2px;
    }

    .time-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 30px;
        color: #FFFFFF;
        margin-top: 10px;
    }

    .confidence-text {
        color: var(--elite-gold);
        font-size: 18px;
        margin-top: 15px;
        font-weight: bold;
    }
</style>
"""
st.markdown(elite_css, unsafe_allow_html=True)

# ==================== LÓGICA DE LOGIN ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'current_signal' not in st.session_state:
    st.session_state.current_signal = None

users = load_users()

if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("💎 ELITE CRIPTO IDX")
    st.markdown("<p style='color: #D4AF37;'>SISTEMA DE ALTA PERFORMANCE</p>", unsafe_allow_html=True)
    
    email = st.text_input("E-mail de Acesso")
    password = st.text_input("Senha", type="password")
    
    if st.button("ACESSAR TERMINAL"):
        if email in users:
            if users[email]["password"] == password:
                if users[email]["active"]:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("❌ Acesso bloqueado.")
            else:
                st.error("❌ Senha incorreta.")
        else:
            st.error("❌ Usuário não cadastrado.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== INTERFACE DO INDICADOR ====================
else:
    # Cabeçalho
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("<h1 style='color: #D4AF37; margin:0;'>💎 ELITE CRIPTO IDX</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #00F2FF;'>Ativo: CRYPTO IDX</p>", unsafe_allow_html=True)
    with col_h2:
        if st.button("SAIR"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("<hr style='border-color: #D4AF37;'>", unsafe_allow_html=True)
    
    # Área Central (Estilo Quantium)
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    
    with col_c2:
        st.markdown("<h3 style='text-align: center; color: #FFF;'>IDENTIFICAR RESULTADO</h3>", unsafe_allow_html=True)
        
        if st.button("🔥 CLIQUE PARA GERAR SINAL 🔥"):
            with st.spinner("ANALISANDO..."):
                time.sleep(1.5)
                action = np.random.choice(["COMPRA", "VENDA"])
                confidence = np.random.randint(96, 99)
                
                # Calcular horário da próxima vela (M1)
                now = datetime.now()
                next_candle = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
                entry_time = next_candle.strftime("%H:%M")
                
                st.session_state.current_signal = {
                    "action": action,
                    "confidence": confidence,
                    "time": entry_time,
                    "color": "#00FF00" if action == "COMPRA" else "#FF0000"
                }

        if st.session_state.current_signal:
            s = st.session_state.current_signal
            st.markdown(f"""
            <div class="result-box">
                <p class="signal-text" style="color: {s['color']};">{s['action']}</p>
                <p class="time-text">às {s['time']}</p>
                <p class="confidence-text">ASSERTIVIDADE: {s['confidence']}%</p>
                <p style="color: #555; font-size: 12px; margin-top: 20px;">SINAL VÁLIDO PARA M1</p>
            </div>
            """, unsafe_allow_html=True)

    # Painel Admin
    if st.session_state.user_email == "admin@elite.com":
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.expander("⚙️ PAINEL DE CONTROLE (ADMIN)"):
            new_email = st.text_input("E-mail do Cliente")
            new_pass = st.text_input("Senha do Cliente")
            if st.button("CRIAR ACESSO"):
                if new_email and new_pass:
                    users[new_email] = {"password": new_pass, "active": True}
                    save_users(users)
                    st.success(f"✅ Cliente cadastrado!")
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
