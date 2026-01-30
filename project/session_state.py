import streamlit as st
from models.stock.stock import Stock
 
def init_session_state():
    
    for key in ["estoque", "produtos", "reservas", "clientes", "funcionarios", "entregas"]:
        if key not in st.session_state:
            st.session_state[key] = []

    if "responsavel_estoque" not in st.session_state:
        st.session_state.responsavel_estoque = "João Silva"

    if "capacidade_total" not in st.session_state:
        st.session_state.capacidade_total = 10

    if "stock_obj" not in st.session_state:
        st.session_state.stock_obj = Stock(10, "João Silva", "Estoque Central")
        
    if "produtos" not in st.session_state:
        st.session_state.produtos = { 
            "Arroz": {"preco": 25.00, "promocao": 20.00}, 
            "Feijão": {"preco": 15.00, "promocao": None},
            "Café": {"preco": 18.00, "promocao": 16.50}, 
        }
