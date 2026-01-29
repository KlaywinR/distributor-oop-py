import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from session_state import init_session_state
from modules.pages.start_page import print_start_page
from modules.pages.stock_page import print_stock_page
from modules.pages.orders_page import print_orders_page
from modules.pages.management_page import print_management_page
from modules.pages.seller_page import print_seller_page
from modules.pages.deliveries_page import print_deliveries_page
from modules.pages.driver_page import print_driver_page
from modules.pages.client_page import print_client_page


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
    print_start_page()
elif menu == "Área Cliente":
    print_client_page()
elif menu == "Área Estoque":
    print_stock_page()
elif menu == "Área Pedidos":
    print_orders_page()
elif menu == "Área Gerente":
    print_management_page()
elif menu == "Área Vendedor":
    print_seller_page()
elif menu == "Área Motorista":
    print_driver_page()
elif menu == "Área Entregas":
    print_deliveries_page()
