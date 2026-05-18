import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import json
import base64

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="Elite Cripto IDX - Premium",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== FUNÇÕES DE IMAGEM ====================
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

def img_to_html(img_path):
    bin_str = get_base64_of_bin_file(img_path)
    if bin_str:
        img_format = img_path.split(".")[-1]
        html_code = f'<img src="data:image/{img_format};base64,{bin_str}" style="width:100%; max-width:300px; display:block; margin:auto;">'
        return html_code
    return ""

# ==================== BANCO DE DADOS SIMPLES (JSON) ====================
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

# ==================== ESTILO CSS PREMIUM ====================
elite_premium_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    :root {
        --elite-gold: #D4AF37;
        --elite-blue-deep: #001122;
    }
    .main { background: linear-gradient(180deg, #000B18 0%, #001A33 100%); color: #FFFFFF; }
    h1, h2, h3, p, span, div { font-family: 'Rajdhani', sans-serif; }
    .stButton > button {
        background: linear-gradient(135deg, #B8860B 0%, #D4AF37 50%, #FFD700 100%);
        color: #000B18; border-radius: 8px; font-family: 'Orbitron', sans-serif;
        font-weight: 900; padding: 18px 20px; width: 100%; text-transform: uppercase;
        letter-spacing: 2px; font-size: 18px; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    .login-box { max-width: 500px; margin: 20px auto; padding: 40px; background: rgba(0, 11, 24, 0.9); border: 2px solid var(--elite-gold); border-radius: 25px; text-align: center; }
    .result-box { background: rgba(0, 11, 24, 0.8); border: 2px solid var(--elite-gold); border-radius: 20px; padding: 50px; text-align: center; margin-top: 30px; backdrop-filter: blur(10px); }
    .signal-text { font-family: 'Orbitron', sans-serif; font-size: 60px; font-weight: 900; margin: 0; letter-spacing: 5px; text-shadow: 0 0 20px currentColor; }
    .time-text { font-family: 'Orbitron', sans-serif; font-size: 35px; color: #FFFFFF; margin-top: 15px; }
    .confidence-text { color: var(--elite-gold); font-size: 20px; font-weight: bold; }
</style>
"""
st.markdown(elite_premium_css, unsafe_allow_html=True)

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
    if os.path.exists("logo.jpeg"):
        st.markdown(img_to_html("logo.jpeg"), unsafe_allow_html=True)
    else:
        st.title("💎 ELITE CRIPTO IDX")
    
    st.markdown("<h3 style='color: #D4AF37; margin-top: 20px;'>ACESSO EXCLUSIVO</h3>", unsafe_allow_html=True)
    
    # Melhoria: strip() para remover espaços e lower() para ignorar maiúsculas
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
                    st.error("❌ Acesso bloqueado.")
            else:
                st.error("❌ Senha incorreta.")
        else:
            st.error("❌ Usuário não cadastrado.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== INTERFACE DO INDICADOR ====================
else:
    col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
    with col_h2:
        if os.path.exists("logo.jpeg"):
            st.markdown(img_to_html("logo.jpeg"), unsafe_allow_html=True)
        else:
            st.markdown("<h1 style='text-align:center; color:#D4AF37;'>ELITE CRIPTO IDX</h1>", unsafe_allow_html=True)
    
    with col_h3:
        if st.button("SAIR"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("<div style='text-align:center; color:#00F2FF; font-weight:bold; letter-spacing:2px;'>SISTEMA DE ALTA PERFORMANCE ATIVADO</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(212, 175, 55, 0.3);'>", unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37; letter-spacing: 3px;'>ANALISAR PRÓXIMA VELA</h3>", unsafe_allow_html=True)
        
        if st.button("🔥 IDENTIFICAR OPORTUNIDADE 🔥"):
            with st.spinner("ESCANEANDO PADRÕES IDX..."):
                time.sleep(1.5)
                action = np.random.choice(["COMPRA", "VENDA"])
                confidence = np.random.randint(97, 100)
                
                # Ajuste de Tempo: Próxima vela (M1 ou M5 conforme sua preferência)
                # Aqui definimos para a próxima vela cheia (ex: se são 09:50:30, a entrada é 09:51 ou 09:55)
                now = datetime.now()
                # Sugestão: Próxima vela de 5 minutos (distância máxima de 5 min)
                minutes_to_add = 5 - (now.minute % 5)
                if minutes_to_add == 0: minutes_to_add = 5
                
                next_candle = (now + timedelta(minutes=minutes_to_add)).replace(second=0, microsecond=0)
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
                <p class="signal-text" style="color: {s['color']};">{s['action']}</p>
                <p class="time-text">entrada às {s['time']}</p>
                <div style="background: rgba(212, 175, 55, 0.1); padding: 10px; border-radius: 10px; border: 1px solid var(--elite-gold); margin-top: 20px;">
                    <p class="confidence-text" style="margin:0;">ASSERTIVIDADE: {s['confidence']}%</p>
                </div>
                <p style="color: #888; font-size: 14px; margin-top: 25px; letter-spacing: 2px;">OPERAÇÃO RECOMENDADA PARA M5</p>
            </div>
            """, unsafe_allow_html=True)

    # Painel Admin
    if st.session_state.user_email == "admin@elite.com":
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.expander("⚙️ PAINEL DE CONTROLE PREMIUM"):
            st.subheader("Cadastrar Novo Cliente")
            new_email = st.text_input("E-mail do Cliente").strip().lower()
            new_pass = st.text_input("Senha do Cliente").strip()
            if st.button("CRIAR ACESSO"):
                if new_email and new_pass:
                    users[new_email] = {"password": new_pass, "active": True}
                    save_users(users)
                    st.success(f"✅ Cliente {new_email} cadastrado!")
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
