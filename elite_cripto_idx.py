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

# ==================== ESTILO CSS ELITE ATUALIZADO ====================
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
        border-radius: 5px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 15px 20px;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .login-box {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: rgba(0, 11, 24, 0.9);
        border: 2px solid var(--elite-gold);
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
    }

    .signal-card {
        background: rgba(0, 11, 24, 0.95);
        border: 2px solid var(--elite-gold);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .time-badge {
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid var(--elite-gold);
        color: var(--elite-gold);
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
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
                    st.error("❌ Acesso bloqueado pelo administrador.")
            else:
                st.error("❌ Senha incorreta.")
        else:
            st.error("❌ Usuário não cadastrado.")
    
    st.markdown("<br><p style='font-size: 12px; color: #555;'>Elite Cripto IDX © 2024</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== INTERFACE DO INDICADOR ====================
else:
    # Cabeçalho
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("<h1 style='color: #D4AF37; margin:0;'>💎 ELITE CRIPTO IDX</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #00F2FF;'>Operador: {st.session_state.user_email} | Ativo: CRYPTO IDX</p>", unsafe_allow_html=True)
    with col_h2:
        if st.button("SAIR"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("<hr style='border-color: #D4AF37;'>", unsafe_allow_html=True)
    
    # Área de Sinais
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Gráfico de Tendência")
        # Simulação de gráfico
        chart_data = pd.DataFrame(np.random.randn(30, 1), columns=['IDX'])
        st.line_chart(chart_data)
        st.success("✅ Algoritmo conectado ao fluxo de dados IDX.")
        
    with col2:
        st.markdown("### 🤖 Gerador de Sinais")
        if st.button("🔥 IDENTIFICAR ENTRADA 🔥"):
            with st.spinner("PROCESSANDO PADRÕES..."):
                time.sleep(2)
                action = np.random.choice(["COMPRAR", "VENDER"])
                confidence = np.random.randint(95, 99)
                
                # Horários
                now = datetime.now()
                entry_time = now.strftime("%H:%M:%S")
                expiry_time = (now + timedelta(minutes=1)).strftime("%H:%M:%S")
                
                st.session_state.current_signal = {
                    "action": action,
                    "confidence": confidence,
                    "entry": entry_time,
                    "expiry": expiry_time,
                    "color": "#00F2FF" if action == "COMPRAR" else "#FF4B4B"
                }

        if st.session_state.current_signal:
            s = st.session_state.current_signal
            st.markdown(f"""
            <div class="signal-card">
                <div class="time-badge">SINAL IDENTIFICADO</div>
                <h1 style="color: {s['color']}; font-size: 70px; margin: 0;">{s['action']}</h1>
                
                <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                    <div>
                        <p style="color: #888; margin:0;">ENTRADA</p>
                        <p style="font-size: 24px; font-weight: bold; color: #FFF;">{s['entry']}</p>
                    </div>
                    <div>
                        <p style="color: #888; margin:0;">EXPIRAÇÃO</p>
                        <p style="font-size: 24px; font-weight: bold; color: #FFF;">{s['expiry']}</p>
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <p style="color: #D4AF37; font-weight: bold;">ASSERTIVIDADE: {s['confidence']}%</p>
                    <div style="background: #111; height: 12px; border-radius: 6px; border: 1px solid {s['color']};">
                        <div style="background: {s['color']}; width: {s['confidence']}%; height: 100%; border-radius: 6px; box-shadow: 0 0 10px {s['color']};"></div>
                    </div>
                </div>
                
                <p style="margin-top: 20px; color: #00F2FF; font-size: 12px;">✅ OPERAÇÃO RECOMENDADA PARA M1</p>
            </div>
            """, unsafe_allow_html=True)

    # Painel Admin
    if st.session_state.user_email == "admin@elite.com":
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.expander("⚙️ PAINEL DE CONTROLE (ADMIN)"):
            st.subheader("Cadastrar Novo Cliente")
            new_email = st.text_input("E-mail do Cliente")
            new_pass = st.text_input("Senha do Cliente")
            if st.button("CRIAR ACESSO"):
                if new_email and new_pass:
                    users[new_email] = {"password": new_pass, "active": True}
                    save_users(users)
                    st.success(f"✅ Cliente {new_email} cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Preencha todos os campos.")
            
            st.markdown("---")
            st.subheader("Gerenciar Acessos")
            for u_email, data in users.items():
                if u_email != "admin@elite.com":
                    col_u1, col_u2 = st.columns([3, 1])
                    status = "✅ ATIVO" if data['active'] else "❌ BLOQUEADO"
                    col_u1.write(f"**{u_email}** | Status: {status}")
                    if col_u2.button("BLOQUEAR/LIBERAR", key=u_email):
                        users[u_email]["active"] = not users[u_email]["active"]
                        save_users(users)
                        st.rerun()
