import streamlit as st
from datetime import date
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from project.models.pallet import Pallet
from project.abstracts.loyalty_system import LoyaltySystem
from project.models.mannager import Manager
from project.models.client import Client



if "estoque" not in st.session_state:
    st.session_state.estoque = []

if "produtos" not in st.session_state:
    st.session_state.produtos = []

if "reservas" not in st.session_state:
    st.session_state.reservas = []
    

manager = Manager("Joao Silva", 123456)

st.set_page_config(
    page_title="SISTEMA DE GESTÃO COMERCIAL E LOGÍSTICA DE DISTRIBUIDORA",
    layout="wide"
)

menu = st.sidebar.radio(
    "Menu",
    ["Início", "Área do Cliente", "Área de Produtos", "Estoque", "Pedidos", "Gerência Geral"]
)


def start_page():
    st.subheader("Início")
    st.write("Tela inicial do sistema")
    
def product_page():
    st.subheader("Gestão de Produtos")

    st.write("Produtos cadastrados:")
    for p in st.session_state.produtos:
        st.write(f"- {p['nome']} | R${p['preco']} | Quant: {p['quantidade']}")

    if "mostrar_form" not in st.session_state:
        st.session_state.mostrar_form = False

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cadastrar Produto"):
            st.session_state.mostrar_form = True

    with col2:
        if st.button("Adicionar Preço Promocional"):
            for p in st.session_state.estoque:
                p.preco_promocional = p.preco_unitario * 0.9  # 10% de desconto
            st.success("Preço promocional aplicado automaticamente!")

    if st.session_state.mostrar_form:
        with st.form("form_produto"):
            name = st.text_input("Nome do produto:")
            price = st.number_input("Preço unitário:")
            quantity = st.number_input("Quantidade:")

            submitted = st.form_submit_button("Cadastrar")
            if submitted:
                st.session_state.produtos.append({
                    'nome': name,
                    'preco': price,
                    'quantidade': quantity
                })
                st.success(f"Produto '{name}' cadastrado com sucesso!")



def client_page():
    st.subheader("Clientes")
    st.write("Bem-vindo(a) à distribuidora! Faça suas compras ou consulte promoções.")

    if "client" not in st.session_state:
        st.session_state.client = Client(
            "Atacadão", 123456, 12453, 10000,
            "Preferências", "Ativo",
            date.today(), "Endereço", "Telefone", "Tipo"
        )
    client = st.session_state.client

    #Comprar produtos
    with st.container():
        st.markdown("### 🛒 Comprar Produtos")

        with st.form("comprar_produto"):
            produto = st.text_input("Produto que deseja comprar")
            submitted = st.form_submit_button("Comprar")

        if submitted:
            if produto in st.session_state.produtos:
                client.buy(produto)
                st.success(f"Compra de '{produto}' realizada com sucesso!")
            else:
                st.error("Produto não encontrado")

            
    with st.container():
        st.markdown("### 📊 Desconto por volume")

        with st.form("desconto_volume"):
            quantity_pallets = st.number_input("Quantidade de pallets", min_value=1)
            submitted = st.form_submit_button("Aplicar desconto")

        if submitted:
            if client.volume_discount(quantity_pallets):
                st.success("Desconto aplicado com sucesso!")


    with st.container():
        st.markdown("### ⭐ Adicionar Pontos Fidelidade")

        with st.form("pontos_fidelidade"):
            buy_value = st.number_input("Valor da compra", min_value=0.0)
            submitted = st.form_submit_button("Adicionar pontos")

        if submitted:
            if client.add_loyalty_points(buy_value):
                st.success("Pontos adicionados com sucesso!")


    with st.container():
        st.markdown("### 🎁Reivindicar Pontos")
        if st.button("🎁Reivindicar Pontos"):
            st.info("Funcionalidade de resgate de pontos.")
            client = Client("Atacadão", 123456, 12453, 10000, "Preferências", "Ativo", date.today(), "Endereço", "Telefone", "Tipo")
            if client.claim_points():
                st.success("Pontos resgatados com sucesso!") 

    with st.container():
        st.markdown("### 🔍Checar Promoções")
        if st.button("🔍Checar Promoções"):
            st.info("Funcionalidade de promoções em desenvolvimento.")
            client = Client("Atacadão", 123456, 12453, 10000, "Preferências", "Ativo", date.today(), "Endereço", "Telefone", "Tipo")
            if client.check_promotion(buy_value=st.number_input("Valor da compra:")):
                st.success("Promoção verificada com sucesso!")

    with st.container():
        st.markdown("### 💬 Avaliar Serviço")

        with st.form("avaliacao_servico"):
            rating = st.number_input("Avaliação (1 a 5)", 1, 5)
            comment = st.text_area("Comentário")
            submitted = st.form_submit_button("Enviar avaliação")

        if submitted:
            if client.evaluate_service(rating, comment):
                st.success("Avaliação enviada com sucesso!")


                comment = st.text_area("Deixe sua avaliação:")
                if st.button("Enviar Avaliação"):
                    if client.evaluate_service(rating=rating, comment=comment):
                        st.success("Avaliação enviada com sucesso!")

   
    
def orders_page():
    st.subheader("Pedidos")
    st.write("Tela de pedidos")
    
def stock_page():
    
    st.subheader("Estoque")
    st.write("Acompanhamento do estoque")

    st.subheader("📦 Estoque")
    col1, col2, col3, col4 = st.columns(4)

    # Adicionar Pallet
    with col1:
        if st.button("Adicionar Pallet"):
            with st.form("form_add_pallet"):
                nome = st.text_input("Nome do Produto:")
                quantidade = st.number_input("Quantidade de pallets:", min_value=1)
                preco = st.number_input("Preço unitário do pallet:", min_value=0.0, format="%.2f")
                validade = st.date_input("Data de validade do pallet:")

                submitted = st.form_submit_button("Adicionar")
                if submitted:
                    novo_pallet = Pallet(nome, quantidade, preco, validade)
                    if novo_pallet.is_active():
                        st.session_state.estoque.append(novo_pallet)
                        st.success(f"Pallet '{nome}' adicionado! Quantidade: {quantidade}")
                    else:
                        st.error(f"Pallet '{nome}' está vencido e não foi adicionado.")
                    st.info(f"Total de pallets no estoque: {len(st.session_state.estoque)}")

    # Remover Pallet
    with col2:
        if st.button("Remover Pallet"):
            nomes_estoque = [p.nome for p in st.session_state.estoque]
            if nomes_estoque:
                nome_remover = st.selectbox("Escolha o pallet para remover:", nomes_estoque)
                if st.button("Confirmar remoção"):
                    st.session_state.estoque = [p for p in st.session_state.estoque if p.nome != nome_remover]
                    st.success(f"Pallet '{nome_remover}' removido!")
                    st.info(f"Total de pallets no estoque: {len(st.session_state.estoque)}")
            else:
                st.warning("Não há pallets no estoque para remover.")
 
    # Mostrar Estoque
    with col3:
        if st.button("Mostrar Estoque"):
            if st.session_state.estoque:
                total_valor = sum(p.quantidade * p.preco_unitario for p in st.session_state.estoque)
                for p in st.session_state.estoque:
                    st.write(f"- {p.nome} | Quant: {p.quantidade} | Preço Unit: R${p.preco_unitario:.2f} | Ativo: {p.is_active()}")
                    if hasattr(p, "preco_promocional") and p.preco_promocional:
                        st.write(f"  -> Preço Promocional: R${p.preco_promocional:.2f}")
                st.success(f"Valor total do estoque: R${total_valor:.2f}")
                st.info(f"Total de pallets: {len(st.session_state.estoque)}")
            else:
                st.warning("O estoque está vazio.")

    # Reserva de pallets (compra por encomenda)
    with col4:
        if st.button("Reservar Pallet"):
            with st.form("form_reserva"):
                cliente = st.text_input("Nome do Cliente:")
                produto = st.selectbox("Produto:", [p.nome for p in st.session_state.estoque])
                quantidade = st.number_input("Quantidade a reservar:", min_value=1)
                submitted = st.form_submit_button("Reservar")
                if submitted:
                    st.session_state.reservas.append({
                        "cliente": cliente,
                        "produto": produto,
                        "quantidade": quantidade,
                        "data": date.today()
                    })
                    st.success(f"{quantidade} pallet(s) de {produto} reservado(s) para {cliente}!")

# -------------------- Gerência Geral --------------------
def general_management(manager):
    st.subheader("Gerência Geral")
    st.write("Resumo do sistema:")

    st.write("📦 Estoque:")
    st.write(manager.ver_estoque(st.session_state.estoque))

    st.write("👥 Clientes:")
    st.write(manager.lista_clientes())

    st.write("🧑‍💼 Vendedores:")
    st.write(manager.lista_vendedores())

    st.write("🚚 Motoristas:")
    st.write(manager.lista_motoristas())

if menu == "Início":
    start_page()
elif menu == "Área de Produtos":
    product_page()
elif menu == "Área do Cliente":
    client_page()
elif menu == "Estoque":
    stock_page()
elif menu == "Pedidos":
    orders_page()
elif menu == "Gerência Geral":
    general_management(manager)