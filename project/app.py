import streamlit as st
from ..streamlit.state.session_state import init_session_state


from ..streamlit.pages.start_page import start_page
from ..streamlit.pages import stock_page
from ..streamlit.pages import orders_page
from ..streamlit.pages import management_page
from ..streamlit.pages import seller_page
from ..streamlit.pages import deliveries_page
from ..streamlit.pages import driver_page
from ..streamlit.pages import client_page


st.set_page_config(
    page_title="Sistema de Gestão Comercial e Logística",
    layout="wide"
)

init_session_state()

menu = st.sidebar.radio(
    "Menu",
    [
        "Tela Inicial",
        "Área Cliente",
        "Área Estoque",
        "Área Pedidos",
        "Área Gerente",
        "Área Vendedor",
        "Área Motorista",
        "Área Entregas"
    ]
)

if menu == "Tela Inicial":
    start_page()
elif menu == "Área Cliente":
    client_page()
elif menu == "Área Estoque":
    stock_page()
elif menu == "Área Pedidos":
    orders_page()
elif menu == "Área Gerente":
    management_page()
elif menu == "Área Vendedor":
    seller_page()
elif menu == "Área Motorista":
    driver_page()
elif menu == "Área Entregas":
    deliveries_page()
