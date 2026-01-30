import streamlit as st
from datetime import date
from project.models.client import Client



def print_client_page():
    st.subheader("Clients")
    st.markdown("___")
    st.write("Bem-vindo(a) à distribuidora! Faça suas compras ou consulte promoções.")
    

    if "client" not in st.session_state:
        st.session_state.client = Client(
            "Atacadão Queiroz", 123456, 12453, 10000,
            "Preferências", "Ativo",
            date.today(), "Endereço", "Telefone", "Tipo"
        )
    client = st.session_state.client
    
    with st.form("comprar_produto"):
        produto = st.text_input("Digite o produto que deseja comprar")
        submitted = st.form_submit_button("Efetuar Compra")
        
    if submitted:
        if produto in st.session_state.produtos:
            client.buy(produto)
            st.success(f"Compra de '{produto}' realizada com sucesso!")
        else:
            st.success(f"Compra de '{produto}' realizada com sucesso!")

    with st.form("desconto_volume"):
        quantity_pallets = st.number_input("Quantidade de pallets", min_value=1)
        submitted = st.form_submit_button("Aplicar desconto")
        
    if submitted:
        desconto = client.volume_discount(quantity_pallets)
        if desconto > 0:
            st.success(f"Desconto aplicado com sucesso! | Valor do Desconto: R$ {desconto}")
        else:
            st.warning("Mensagem do Sistema: Não existe desconto disponível para esta quantidade de pallets.")


    with st.form("pontos_fidelidade"):
        buy_value = st.number_input("Valor da compra", min_value=0.0)
        submitted = st.form_submit_button("Adicionar pontos ao valor da compra")
        
    if submitted:
        pontos = client.add_loyalty_points(buy_value)
        if pontos > 0:
            st.success(f"Pontos adicionados com sucesso | Total: {pontos}")
        else:
            st.warning("Mensagem do Sistema: Nenhum ponto foi acumulado para o valor da sua compra.")
        
    if st.button("Desejo Reivindicar Pontos"):
        pontos = client.claim_points()
        if pontos > 0:
            st.success(f"Pontos resgatados com sucesso | Total Resgatado: {pontos}")
        else:
            st.warning("Mensagem do Sistema: Você não possui pontos para resgate.")

    st.subheader("Promoções")
    
    if st.session_state.produtos:
        produto = st.selectbox(
            "Selecione o produto para verificar promoção:", 
            list(st.session_state.produtos.keys()) 
        )
        
    if st.button("Desejo Ver Promoções"):
            dados = st.session_state.produtos[produto]    
            if dados["promocao"] is not None:
                st.success (
                    f"O produto {produto} se encontra em promoção. "
                    )
            else: 
                st.warning(f"Mensagem do Sistema: O produto {produto} não possui promoção ativa no momento.")
    else:
        st.warning("Mensagem do Sistema: Não existe nenhum produto cadastrado no sistema.")

    with st.form("avaliacao_servico"):
        """
        Avaliação de serviço
        """
        rating = st.number_input("Avalie de 1 a 5", 1, 5)
        comment = st.text_area("Criar Comentário")
        submitted = st.form_submit_button("Enviar Comentário")
    if submitted and client.evaluate_service(rating, comment):
        st.success("A avaliação foi feita com sucesso.")
        