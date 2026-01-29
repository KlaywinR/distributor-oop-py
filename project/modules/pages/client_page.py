import streamlit as st
from datetime import date
from project.models.client import Client



def print_client_page():
    st.subheader("Clients")
    st.markdown("___")
    st.write("Bem-vindo(a) à distribuidora! Faça suas compras ou consulte promoções.")
    
    """
    Verifica se o cliente já está na sessão de estado, caso contrário, cria um novo cliente.
    """
    if "client" not in st.session_state:
        st.session_state.client = Client(
            "Atacadão Queiroz", 123456, 12453, 10000,
            "Preferências", "Ativo",
            date.today(), "Endereço", "Telefone", "Tipo"
        )
    client = st.session_state.client
    
    with st.form("comprar_produto"):
        produto = st.text_input("Nome do produto que deseja comprar")
        submitted = st.form_submit_button("Efetuar Compra")
    if submitted:
        if produto in st.session_state.produtos:
            client.buy(produto)
            st.success(f"Compra de '{produto}' realizada com sucesso!")
        else:
            st.error("Produto não foi encontrado")

    with st.form("desconto_volume"):
        quantity_pallets = st.number_input("Quantidade de pallets", min_value=1)
        submitted = st.form_submit_button("Aplicar desconto")
    if submitted and client.volume_discount(quantity_pallets):
        st.success("Desconto aplicado com sucesso!")


    with st.form("pontos_fidelidade"):
        buy_value = st.number_input("Valor da compra", min_value=0.0)
        submitted = st.form_submit_button("Adicionar pontos")
    if submitted and client.add_loyalty_points(buy_value):
        st.success("Pontos adicionados com sucesso!")

    if st.button("Desejo Reivindicar Pontos") and client.claim_points():
        st.success("Pontos resgatados com sucesso!") 

    if st.button("Desejo Ver Promoções"):
        valor = st.number_input("Valor da compra:")
        if client.check_promotion(buy_value=valor):
            st.success("Promoção verificada com sucesso!")

    with st.form("avaliacao_servico"):
        """
        Avaliação de serviço
        """
        rating = st.number_input("Avalie de 1 a 5", 1, 5)
        comment = st.text_area("Criar Comentário")
        submitted = st.form_submit_button("Enviar Comentário")
    if submitted and client.evaluate_service(rating, comment):
        st.success("A avaliação foi feita com sucesso.")
        