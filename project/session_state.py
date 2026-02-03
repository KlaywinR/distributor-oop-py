import streamlit as st
from models.stock.stock import Stock
from models.product.product import Product
from models.product.product_status import ProductStatus
from datetime import date

def init_session_state():
    
    for key in ["estoque", "produtos", "reservas", "clientes", "funcionarios", "entregas"]:
        if key not in st.session_state:
            st.session_state[key] = []

    if "responsavel_estoque" not in st.session_state:
        st.session_state.responsavel_estoque = "João Silva"

    if "capacidade_total" not in st.session_state:
        st.session_state.capacidade_total = 1000

    if "stock_obj" not in st.session_state:
        st.session_state.stock_obj = Stock(10, "João Silva", "Estoque Central")
        
    if "produtos" not in st.session_state:
        st.session_state.produtos = ["Arroz", "Feijão", "Cimento"]
        
    if "nota_emitida" not in st.session_state:
        st.session_state.nota_emitida = None
        
    if "notas_fiscais" not in st.session_state:
        st.session_state.notas_fiscais = []
        
    if "dashboard" not in st.session_state:
        st.session_state.dashboard = None
        

        

    if "funcionarios" not in st.session_state:
        st.session_state.funcionarios = [
        {"nome": "Carlos", "vendas": 12, "entregas": 5, "promovido": True},
        {"nome": "Ana", "vendas": 8, "entregas": 22, "promovido": False},
        {"nome": "João", "vendas": 15, "entregas": 30, "promovido": True}
    ]

        
         
