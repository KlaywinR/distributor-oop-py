import streamlit as st
from modules.pages import client_page
from modules.pages import stock_page
from modules.pages import orders_page
import pandas as pd
import random 

if "nav" not in st.session_state:
    st.session_state["nav"] = "start"

def print_start_page():
    
    st.title("Sistema DistriSys")
    st.markdown("---")

    st.subheader("Olá, seja bem-vindo!")
    st.write("Este é o painel inicial do sistema. Você pode navegar rapidamente para qualquer área e visualizar um resumo de operações.")

    st.subheader("Fast Acess")
    col1, col2, col3 = st.columns(3)
    
    button_style = """
        <style>
        div.stButton > button {
            
            height: 3em;
            width: 100%;
            font-size: 18px;
            font-weight: bold;
            color: black;
            background-color: #fde910;
            border-radius: 10px;
        }
        div.stButton > button:hover {
            background-color: #fde910;
        }
        </style>
    """
    
    st.markdown(button_style, unsafe_allow_html=True)
    
    with col1:
        if st.button("Ver Sumário de Clientes"):
            st.session_state["nav"] = "cliente"
    with col2:
        if st.button("Ver Sumário do Estoque"):
            st.session_state["nav"] = "estoque"
    with col3:
        if st.button("Ver Sumário de Pedidos "):
            st.session_state["nav"] = "pedidos"
    st.markdown("---")

    dados_dashboard = {
        "Clientes": random.randint(20,120),
        "Produtos":  random.randint(30,80),
        "Funcionários": random.randint(5,20),
        "Entregas": random.randint(10,50), 
        "Estoque":  random.randint(40,150)
    }
        
    df = pd.DataFrame(list(dados_dashboard.items()), columns=["Categoria", "Quantidade"])
    
    st.subheader("Summary Geral")
    
    st.markdown("""
        <style>
            .streamlit-expanderHeader {
                font-size: 25px;
                font-weight: bold;
            }
            .css-1aumxhk {
                background-color: #f0f2f6;
            }
        </style>
        """, unsafe_allow_html=True)

    st.bar_chart(df.set_index("Categoria"))
    
    st.markdown("----")
    
    st.subheader("Interaja com o DistriSys")
    username = st.text_input("Digite seu nome:")
    humor = st.selectbox(f"Olá! {username} Como você está se sentindo hoje?", [" Ótimo", "Muito Bem", "Estou Neutro", "Muito Cansado"])
    if st.button("Enviar Respostas"):
        st.success(f"Olá, {username} que bom ter você aqui! Vejo que está se sentindo {humor}. Vamos tornar sua experiência ainda mais produtiva haha!")
    st.markdown("---")

    st.subheader("Dica do Dia")
    tip = [
        "Organize seus pedidos logo cedo para evitar atrasos.",
        "Verifique promoções ativas para aumentar suas vendas.",
        "Mantenha o estoque atualizado para evitar rupturas.",
        "Clientes satisfeitos são a chave para o sucesso!"
    ]
    st.info(random.choice(tip))

