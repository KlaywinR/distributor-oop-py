import streamlit as st
from datetime import date
from project.models.client import Client
from tabulate import tabulate
import pandas as pd 

def print_client_page():
    st.write("Bem-vindo(a) à distribuidora! Faça suas compras ou consulte promoções.")
   
    if "client" not in st.session_state:
        st.session_state.client = Client(
            name="IFRN DISTRIBUIDORA LTDA",
            cnpj=12345678901234,
            id_client=6775,
            credit_limit=1200,
            costumer_preferences="Secos",
            client_status="ACTIVE",
            registration_date=date.today(),
            address="Santa Luz - RN",
            phone="12 58675-8965",
            client_type="CNPJ",
            loyalty_points=120
        )
        
    client = st.session_state.client
    
    with st.form("comprar_produto"):
        produto = st.text_input("Digite o produto que deseja comprar")
        quantity_pallets = st.number_input("Quantidade de pallets", min_value=1)
        unit_value = st.number_input("Valor unitário do pallet", min_value=0.0)
        submitted = st.form_submit_button("Efetuar Compra")
        
        if submitted:
            if produto in client.produtos:
                valor_final = client.buy(produto, quantity_pallets, unit_value)
                st.success(f"Compra de '{produto}' realizada com sucesso! Valor Final: R$ {valor_final:.2f}")
            else:
                st.warning(f"Mensagem do Sistema: O produto '{produto}' não foi encontrado no sistema!")
    
    with st.form("desconto_volume"):
        pallets = st.number_input("Quantidade de pallets para desconto", min_value=1)
        submitted = st.form_submit_button("Aplicar desconto")
        
        if submitted:
            desconto = client.volume_discount(pallets)
            if desconto > 0:
                st.success(f"Mensagem do Sistema: O Desconto foi aplicado - Percentual: {desconto*100:.0f}%")
            else:
                st.info("Mensagem do Sistema: Nenhum desconto disponível para essa quantidade de pallets.")
    
 
    with st.form("pontos_fidelidade"):
        valor_compra = st.number_input("Valor da compra para adicionar pontos", min_value=0.0)
        submitted = st.form_submit_button("Adicionar pontos")
        
        if submitted:
            pontos = client.add_loyalty_points(valor_compra)
            if pontos > 0:
                st.success(f"Pontos adicionados com sucesso! Total de pontos adicionados: {pontos}")
            else:
                st.info("Mensagem do Sistema: Nenhum ponto foi acumulado para o valor informado.")
    
    
    if st.button("Desejo Reivindicar Pontos"):
        pontos = client.claim_points()
        if pontos > 0:
            st.success(f"Pontos resgatados com sucesso! Total resgatado: {pontos}")
        else:
            st.info("Mensagem do Sistema: Você não possui pontos para resgate.")
    
   
    st.subheader("Promoções")
    if client.produtos:
        produto_selecionado = st.selectbox(
            "Selecione o produto para verificar promoção:",
            list(client.produtos.keys())
        )
        
        if st.button("Desejo Ver Promoção"):
            promocao = client.check_promotion(produto_selecionado)
            if promocao:
                st.success(f"O produto '{produto_selecionado}' está em promoção por R$ {promocao:.2f}!")
            else:
                st.info(f"O produto '{produto_selecionado}' não possui promoção no momento.")
    else:
        st.warning("Mensagem do Sistema: Não existem produtos cadastrados no sistema.")
    
   
    st.subheader("Avaliação do Service")
    with st.form("avaliacao_servico"):
        rating = st.number_input("Avalie de 1 a 5", 1, 5)
        comment = st.text_area("Comentário (opcional)")
        submitted = st.form_submit_button("Enviar Avaliação")
        
        if submitted:
            msg = client.evaluate_service(rating, comment)
            st.success(msg)
    

    if st.button("Exibir Resumo do Cliente"):
        resumo = client.summary_client()
        
        st.info(f"Nome: {resumo['Name']}")
        st.info(f"Tipo de Cliente: {resumo['Tipo de Cliente']}")
        
        categoria = resumo["Categoria"]
        st.info(f"Categoria Atual: {categoria['Categoria Atual']}")
        st.info(f"Nível Comercial: {categoria['Nivel Comercial']}")
        st.info(f"Descrição: {categoria['Descrição da Categoria']}")
        st.info("Benefícios:")
        for beneficio in categoria["Benefícios"]:
            st.write(f"- {beneficio}")
        
        st.write(f"Pontos de Fidelidade: {resumo['Pontos de Fidelidade']}")
        
        st.subheader("Histórico de Compras:")
        if resumo["Total de Compras"]:
            tabela = []
            for compra in resumo["Total de Compras"]:
                tabela.append([
                    compra['Date'].strftime('%d/%m/%Y'),
                    compra['Product'],
                    compra['Quantity'],
                    f"R$ {compra['Final Value']:.2f}"
                ])
            
            df = pd.DataFrame(tabela)
            st.table(df)
        else:
            st.success("Mensagem do Sistema: Sem compras registradas.")
