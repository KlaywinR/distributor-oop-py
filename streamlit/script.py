import streamlit as st
from datetime import date
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from project.models.client import Client
from project.models.pallet import Pallet
from project.abstracts.loyalty_system import LoyaltySystem
from project.models.mannager import Manager
from project.models.client import Client



for key in ["estoque", "produtos", "reservas", "clientes", "funcionarios", "entregas"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "responsavel_estoque" not in st.session_state:
    st.session_state.responsavel_estoque = "João Silva" 
    
if "capacidade_total" not in st.session_state:
    st.session_state.capacidade_total = 10
    
manager = Manager("João Lucas Silva", 562662)

st.set_page_config(
    page_title="SISTEMA DE GESTÃO COMERCIAL E LOGÍSTICA DE DISTRIBUIDORA",
    layout="wide"
)

menu = st.sidebar.radio(
    "Menu",
    ["Início", "Área do Cliente", "Nossos Produtos", "Nosso Estoque", "Nossos Pedidos", "Nossa Gerência Geral"]
)

def start_page():
    st.subheader("Início do Sistema")
    st.write("Tela inicial do sistema")

#! deve se colocar a funcção cliente aqui: 
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
#!____________________________________________

#! ---- funcção produto ________________________
def product_page():
    st.subheader("Gestão de Produtos")
    st.write("Produtos cadastrados:")
    for p in st.session_state.produtos:
        st.write(f"- {p['nome']} | R${p['preco']} | Quant: {p['quantidade']}")
#!__________________________________________

#! ----- função estoque -------
def stock_page():
    st.subheader("Nosso Estoque")

    col1, col2, col3, col4 = st.columns(4)

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
                        st.success(f"{quantidade} pallet(s) de '{nome}' adicionado(s) no estoque!")
                        st.info(f"Total de pallets no estoque: {len(st.session_state.estoque)}")
                else:
                        st.error(f"O pallet '{nome}' está vencido e não foi adicionado.")
                    
    with col2:
        if st.button("Remover Pallet"):
            if st.session_state.estoque:
                nomes_estoque = [p.nome for p in st.session_state.estoque]
                nome_remover = st.selectbox("Escolha o pallet para remover:", nomes_estoque)
                confirm = st.checkbox("Confirmar remoção?")
                if confirm:
                    st.session_state.estoque = [p for p in st.session_state.estoque if p.nome != nome_remover]
                    st.success(f"Pallet '{nome_remover}' removido!")
                    st.info(f"Total de pallets no estoque: {len(st.session_state.estoque)}")
        else:
                st.warning("Não há pallets no estoque para remover.")
    with col3:
        if st.button("Mostrar Estoque Completo"):
            if st.session_state.estoque:
                total_valor = 0
                for p in st.session_state.estoque:
                    st.write(f"- {p.nome} | Quant: {p.quantidade} | Preço Unit: R${p.preco_unitario:.2f} | Ativo: {p.is_active()}")
                    total_valor += p.quantidade * p.preco_unitario
            st.success(f"Valor total do estoque: R${total_valor:.2f}")
            st.info(f"Total de pallets: {len(st.session_state.estoque)}")
        else:
            st.warning("O estoque está vazio.")

    with col4:
        if st.button("Informações do Estoque"):
            st.write(f"**Nome do Estoque:** Estoque Principal")
            st.write(f"**Responsável:** {st.session_state.responsavel_estoque}")

            if st.session_state.estoque:
                total_valor = 0
                total_pallets = 0
                for p in st.session_state.estoque:
                    valor_item = p.quantidade * p.preco_unitario
                    st.write(f"- {p.nome} | Quant: {p.quantidade} | Preço Unit: R${p.preco_unitario:.2f} | Valor Total: R${valor_item:.2f}")
                    total_valor += valor_item
                    total_pallets += p.quantidade
                st.success(f"Valor total do estoque: R${total_valor:.2f}")
                st.info(f"Total de pallets no estoque: {total_pallets}")
                st.info(f"Capacidade total do estoque: {st.session_state.capacidade_total} pallets")
            else:
                st.warning("O estoque está vazio.")
#? --------------------------------------------------------------------------

#! PARTE DOS PEDIDOS:
def orders_page():
    st.subheader("Pedidos")
    st.write("Tela de pedidos")
#!_____________________________________


  
#! ======= ABA GERENCIA GERAL =========
def management_page():
    st.subheader("Área do Gerente")
    st.write("Gerenciamento de compras, descontos, funcionários e dashboard.")

    col1, col2, col3, col4, col5,  spacer1, spacer2 = st.columns([1,1,1,1,1,0.5,0.5])

    with col1:
        if st.button("Aprovar Compras  +R$ 5.000"):
            aprovadas = [c for c in st.session_state.clientes if c.get('compra_total', 0) >= 5000]
            if aprovadas:
             st.success(f"Aprovação concedida para {len(aprovadas)} clientes")
        else:
            st.warning("Nenhuma compra acima de R$ 5.000")
            
    with col2:
        if st.button("Aprovar Descontos >= 15%"):
            descontos = [c for c in st.session_state.clientes if c.get('desconto', 0) >= 15]
            if descontos:
                st.success(f"Desconto aprovado para {len(descontos)} clientes")
        else:
                st.warning("Nenhum desconto elegível")
        
    with col3:
        if st.button("Exibir Relatório de Faturamento e Colaboradores"):
            total_faturamento = sum(c.get('compra_total', 0) for c in st.session_state.clientes)
            clientes_ativos = [c for c in st.session_state.clientes if c.get('ativo', True)]
            st.write(f"Faturamento total: R${total_faturamento}")
       
            
            inativos = len(st.session_state.clientes) - len(clientes_ativos)

            dados_grafico = {
            "Quantidade": [len(clientes_ativos), inativos],
            "Categoria": ["Ativos", "Inativos"],
            "Cor": ["#4CAF50", "#F44336"]  # Verde para ativos, vermelho para inativos
        }

        for i in range(2):
            st.progress(dados_grafico["Quantidade"][i] / max(dados_grafico["Quantidade"] + [1]))  # barra proporcional
            st.markdown(f"<span style='color:{dados_grafico['Cor'][i]}; font-weight:bold;'>{dados_grafico['Categoria'][i]}: {dados_grafico['Quantidade'][i]}</span>", unsafe_allow_html=True)
            
    with col4:
        if st.button("Gerenciar Meus Funcionários"):
            promovidos = []
            for f in st.session_state.funcionarios:
                if f.get('vendas',0) > 10 or f.get('entregas',0) > 20:
                    f['promovido'] = True
                    promovidos.append(f['nome'])
                else:
                    f['promovido'] = False
            if promovidos:
                st.success(f"AUTORIZADO: Funcionários promovidos -> {', '.join(promovidos)}")
            else:
                st.warning("Nenhum funcionário promovido")
        

    with col5:
        if st.button("Exibir Dashboard"):
            st.write("Dashboard do Sistema")
            dados_dashboard = {
        "Clientes": len(st.session_state.clientes),
        "Produtos": len(st.session_state.produtos),
        "Funcionários": len(st.session_state.funcionarios),
        "Entregas": len(st.session_state.entregas),
        "Estoque": len(st.session_state.estoque)
    }
    st.bar_chart(dados_dashboard)

    #* navegação na area do gerente

    st.write("---")
    st.subheader("Usar Navegação Rápida")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Ver Meu Estoque"):
            st.write(st.session_state.estoque)
    with col2:
        if st.button("Ver Meus Clientes"):
            st.write(st.session_state.clientes)
    with col3:
        if st.button("Ver Meus Funcionários"):
            st.write(st.session_state.funcionarios)
    with col4:
        if st.button("Ver Minhas Entregas"):
            st.write(st.session_state.entregas)  
#!--------------------------------------------------------------------------------
        
#! ===== MENU FINAL E PRICNIPAL ====

if menu == "Início":
    start_page()
elif menu == "Área do Cliente":
    client_page()
elif menu == "Nossos Produtos":
    product_page()
elif menu == "Nosso Estoque":
    stock_page()
elif menu == "Nossos Pedidos":
    orders_page()
elif menu == "Nossa Gerência Geral":
    management_page()

    


    
