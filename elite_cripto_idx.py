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
        with open(DB_FILE, "r") as f:
            return json.load(f)
    # Usuário padrão para teste
    return {"admin@elite.com": {"password": "123", "active": True}}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# ==================== ESTILO CSS ELITE ====================
elite_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

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
        padding: 10px 20px;
        width: 100%;
    }

    .login-box {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        background: rgba(0, 11, 24, 0.8);
        border: 1px solid var(--elite-gold);
        border-radius: 15px;
        text-align: center;
    }

    .signal-card {
        background: rgba(0, 11, 24, 0.9);
        border: 2px solid var(--elite-gold);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        margin-top: 20px;
    }
</style>
"""
st.markdown(elite_css, unsafe_allow_html=True)

# ==================== LÓGICA DE LOGIN ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

users = load_users()

if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("💎 ELITE CRIPTO IDX")
    st.subheader("Acesso Restrito")
    
    email = st.text_input("E-mail")
    password = st.text_input("Senha", type="password")
    
    if st.button("ENTRAR NO SISTEMA"):
        if email in users:
            if users[email]["password"] == password:
                if users[email]["active"]:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Acesso desativado pelo administrador.")
            else:
                st.error("Senha incorreta.")
        else:
            st.error("Usuário não encontrado.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== INTERFACE DO INDICADOR ====================
else:
    # Barra Superior
    col_a, col_b = st.columns([5, 1])
    with col_a:
        st.title("💎 ELITE CRIPTO IDX")
    with col_b:
        if st.button("SAIR"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")
    
    # Área Principal
    st.info(f"Bem-vindo, {st.session_state.user_email} | Ativo: CRYPTO IDX")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Monitoramento em Tempo Real")
        # Gráfico simulado
        chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['Preço'])
        st.line_chart(chart_data)
        
    with col2:
        st.markdown("### 🤖 Algoritmo de Elite")
        if st.button("IDENTIFICAR OPORTUNIDADE"):
            with st.spinner("Analisando padrões..."):
                time.sleep(2)
                action = np.random.choice(["COMPRAR", "VENDER"])
                confidence = np.random.randint(94, 99)
                expiry = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M:%S")
                
                color = "#00F2FF" if action == "COMPRAR" else "#FF4B4B"
                
                st.markdown(f"""
                <div class="signal-card">
                    <h1 style="color: {color}; font-size: 60px;">{action}</h1>
                    <p style="font-size: 24px; color: #D4AF37;">ASSERTIVIDADE: {confidence}%</p>
                    <p style="font-size: 18px;">VÁLIDO ATÉ: {expiry}</p>
                    <div style="background: #111; height: 10px; border-radius: 5px; margin-top: 10px;">
                        <div style="background: {color}; width: {confidence}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Painel Admin (Apenas visível para o admin@elite.com)
    if st.session_state.user_email == "admin@elite.com":
        st.markdown("---")
        st.subheader("⚙️ Painel do Administrador")
        
        with st.expander("Gerenciar Usuários"):
            new_email = st.text_input("Novo E-mail")
            new_pass = st.text_input("Nova Senha")
            if st.button("CRIAR USUÁRIO"):
                users[new_email] = {"password": new_pass, "active": True}
                save_users(users)
                st.success("Usuário criado!")
            
            st.write("Lista de Usuários:")
            for u_email, data in users.items():
                col_u1, col_u2 = st.columns([3, 1])
                col_u1.write(f"{u_email} (Ativo: {data['active']})")
                if col_u2.button("Alternar Acesso", key=u_email):
                    users[u_email]["active"] = not users[u_email]["active"]
                    save_users(users)
                    st.rerun()
