import streamlit as st
from datetime import date
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from project.models.pallet import Pallet
from project.models.mannager import Manager


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

st.sidebar.markdown("## Menu Principal") 
menu = st.sidebar.radio( "Escolha uma seção:",
                        [ "Tela Inicial", 
                         "Área do Cliente", 
                         "Área de Produtos", 
                         "Área de Estoque", 
                         "Ver Pedidos", 
                         "Gerência Geral" ]) 

def start_page():
    st.subheader("Início do Sistema")
    st.write("Tela inicial do sistema")

#! deve se colocar a funcção cliente aqui: 
def client_page():
    st.subheader("Clientes")
    st.write("Bem-vindo(a) à distribuidora! Faça suas compras ou consulte promoções.")
#!____________________________________________

#!____________ FUNÇÃO PRODUTO __________________________________________________________-
def product_page():
    st.subheader("🛒 Gestão de Produtos")

    #* Mostrar todos os pallets disponíveis ---
    if st.button("📦 Mostrar Paletes Disponíveis"):
        if st.session_state.produtos:
            for p in st.session_state.produtos:
                st.write(f"Temos {p['quantidade']} paletes do {p['nome']}")
        else:
            st.warning("Nenhum produto cadastrado no estoque.")

    #* Adicionar preço promocional automaticamente:
    if st.button("💰 Aplicar Preço Promocional Automático"):
        for p in st.session_state.produtos:
            #!  Exemplo de regra interna: 10% de desconto automático
            p["preco_promocional"] = round(p["preco"] * 0.9, 2)
        st.success("Preço promocional aplicado automaticamente em todos os produtos.")

    #* Adição e remoção de paletes: 
    st.markdown("###  Adição/Remoção de Paletes")
    produto_selecionado = st.selectbox("Selecione o produto:", [p["nome"] for p in st.session_state.produtos])
    acao = st.radio("Ação:", ["Adicionar", "Remover"])
    qtd = st.number_input("Quantidade de paletes", min_value=1, step=1)

    if st.button("Executar Ação"):
        for p in st.session_state.produtos:
            if p["nome"] == produto_selecionado:
                if acao == "Adicionar":
                    p["quantidade"] += qtd
                    st.success(f"{qtd} paletes adicionados ao produto {produto_selecionado}.")
                elif acao == "Remover":
                    if p["quantidade"] >= qtd:
                        p["quantidade"] -= qtd
                        st.success(f"{qtd} paletes removidos do produto {produto_selecionado}.")
                        if p["quantidade"] == 0:
                            st.warning(f"O estoque do produto {produto_selecionado} precisa de reposição!")
                    else:
                        st.error("Quantidade insuficiente para remoção.")
                        
    st.markdown("###  Reserva de Paletes (Compra por Encomenda)")
    with st.form("form_reserva"):
        cliente_nome = st.text_input("Nome do Cliente")
        cliente_email = st.text_input("Email do Cliente")
        produto_reserva = st.selectbox("Produto para reserva:", [p["nome"] for p in st.session_state.produtos])
        qtd_reserva = st.number_input("Quantidade de paletes para reserva", min_value=1, step=1)
        reservar = st.form_submit_button("Reservar")

        if reservar:
            st.success(f"Reserva feita para {cliente_nome}: {qtd_reserva} paletes de {produto_reserva}.")

#* Ve se tem promoções
    st.markdown("###  Verify Promoções")
    produto_promocao = st.selectbox("Selecione o produto para verificar/remover promoção:", [p["nome"] for p in st.session_state.produtos])
    if st.button("Remover Promoção"):
        for p in st.session_state.produtos:
            if p["nome"] == produto_promocao:
                if "preco_promocional" in p:
                    del p["preco_promocional"]
                    st.info("Informação do Sistema: A promoção foi removida.")
                else:
                    st.warning("Este produto não possui promoção ativa.")
    if st.button("Verificar Promoção"):
        for p in st.session_state.produtos:
            if p["nome"] == produto_promocao:
                if "preco_promocional" in p:
                    st.success(f"Preço promocional aplicado: R${p['preco_promocional']}")
                else:
                    st.warning("Nenhum preço promocional aplicado.")

#* Sumário geral de informações do produto:
    st.markdown("###  Sumário Geral do Produto")
    produto_info = st.selectbox("Selecione o produto para ver informações:", [p["nome"] for p in st.session_state.produtos])
    if st.button("Mostrar Informações do Produto"):
        for p in st.session_state.produtos:
            if p["nome"] == produto_info:
                st.write(f"   Data de Validade: {p.get('validade', 'Não informado')}")
                st.write(f"   Status: {p.get('status', 'Ativo')}")
                st.write(f"   Preço por Unidade: R${p.get('preco_unidade', p['preco'])}")
                st.write(f"   Preço Atual do Palete: R${p['preco']}")
                st.write(f"   Preço Promocional do Palete: R${p.get('preco_promocional', 'Sem promoção')}")
                st.write(f"   Marca: {p.get('marca', 'Não informado')}")
                st.write(f"   Código de Barras: {p.get('codigo_barras', 'Não informado')}")
                st.write(f"   Categoria: {p.get('categoria', 'Não informado')}")
                st.write(f"   Fornecedor: {p.get('fornecedor', 'Não informado')}")
                st.write(f"   Origem: {p.get('origem', 'Não informado')}")
                st.write(f"   Nome: {p['nome']}")
                st.write(f"   Peso por Unidade: {p.get('peso_unidade', 'Não informado')}")
                st.write(f"   Preço de Custo: R${p.get('preco_custo', 'Não informado')}")
                st.write(f"   Preço Promocional: {p.get('preco_promocional', 'Sem promoção')}")

    #* Gráfico comparativo de paletes por produto: 
    st.markdown("###  Comparativo de Paletes por Produto")
    if st.session_state.produtos:
        dados = {
            "Produto": [p["nome"] for p in st.session_state.produtos],
            "Quantidade": [p["quantidade"] for p in st.session_state.produtos]
        }
        st.bar_chart(dados)
    else:
        st.warning("Nenhum produto cadastrado para gerar gráfico.")
#!______________________________________________________________________________________________________________



#! ------ FUNÇÃO PEDIDO -----------------------------------------------------------------------------------------
def stock_page():
    st.subheader("  Seja Bem Vindo ao Nosso Estoque")


    st.markdown("###  Quero colocar Paletes")
    with st.form("form_add_pallet"):
        nome = st.text_input("Nome do Pallet") 
        quantidade = st.number_input("Quantidade", min_value=1, step=1) 
        valor_unitario = st.number_input("Valor Unitário (R$)", min_value=0.0, step=0.01) 
        is_active = st.checkbox("Pallet está ativo (não vencido)?", value=True) 
        submitted = st.form_submit_button("Pôr ao Estoque")

        if submitted: 
            if is_active: 
                novo_pallet = { 
                    "nome": nome,
                    "quantidade": quantidade,
                    "valor_unitario": valor_unitario,
                    "is_active": is_active
                }
                st.session_state.estoque.append(novo_pallet)
                st.success(f"{quantidade} pallets de {nome} adicionados ao estoque.") 
            else:
                st.error(f"O pallet '{nome}' está vencido e não pode ser adicionado.")

        #* remove paletes:
    st.markdown("###   Remoção de Paletes") 
    if st.session_state.estoque: 
        pallet_remover = st.selectbox("Selecione o pallet para remover:", 
                                      [p["nome"] for p in st.session_state.estoque])
        confirmar = st.checkbox("Confirmar remoção do pallet selecionado") 
        if st.button("Remover"):
            if confirmar: 
                st.session_state.estoque = [p for p in st.session_state.estoque if p["nome"] != pallet_remover]
                st.success(f"Pallet '{pallet_remover}' removido com sucesso.") 
            else:
                st.warning("Remoção não confirmada. Nenhum pallet foi deletado.") 
    else: 
        st.warning("Estoque vazio. Nenhum pallet para remover.") 

        #* lista paletes e o v.total.
    st.markdown("### Listar Pallets e Valor Total")
    if st.button("Listar Pallets"):
        if st.session_state.estoque:
            valor_total = sum(p["valor_unitario"] * p["quantidade"] for p in st.session_state.estoque)
            
            for p in st.session_state.estoque: 
                st.write(f"- {p['nome']} | Quantidade: {p['quantidade']} | Valor Unitário: R${p['valor_unitario']}")
                
            st.success(f"  Valor total do estoque: R${valor_total}")
        else: 
            st.warning("Estoque vazio.")

    st.markdown("###   Informações do Estoque")
    if st.button("Mostrar Informações"):
        if st.session_state.estoque:
            st.write("### SOBRE O ESTOQUE") 
            st.write(f"  Nome do Estoque: {st.session_state.get('nome_estoque', 'Estoque Principal')}")
            st.write(f"  Responsável: {st.session_state.get('responsavel', 'Funcionário não definido')}") 
            
            valor_total = sum(p["valor_unitario"] * p["quantidade"] for p in st.session_state.estoque)
            quantidade_total = sum(p["quantidade"] for p in st.session_state.estoque)
            capacidade_total = 50  # Limite fixo de 50 pallets
            
            # Listagem resumida
            for p in st.session_state.estoque:
                st.write(f"- {p['nome']} | Quantidade: {p['quantidade']} | Valor Unitário: R${p['valor_unitario']}")
                
            st.success(f"    Valor total dos pallets: R${valor_total}")
            st.info(f"    Capacidade total do estoque: {capacidade_total} pallets") 

        
            ocupacao = quantidade_total / capacidade_total
            st.progress(min(ocupacao, 1.0))
            st.write(f"  Ocupação atual: {quantidade_total}/{capacidade_total} pallets")

            
            dados = {
                "Métrica": ["Receita Total (R$)", "Quantidade Total Vendida"], 
                "Valor": [valor_total, quantidade_total]
            }
            st.bar_chart(dados, x="Métrica", y="Valor")
            
        else: 
            st.warning("Estoque vazio.")
#? -------------------------------------------------------------------------------------------------------



#! = PARTE DOS PEDIDOS ====================================================================================
def orders_page():
    st.subheader("Pedidos")
    st.write("Tela de pedidos")
#!_____________________________________


  
#! ======= ABA GERENCIA GERAL =============================================================================
def management_page():
    st.subheader(" Manager Area")
    st.write("Gerenciamento de compras, descontos, funcionários e dashboard.")


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button(" Aprovar Compras +R$ 5.000"):
            aprovadas = [c for c in st.session_state.clientes if c.get('compra_total', 0) >= 5000]
            if aprovadas:
                for c in aprovadas:
                    st.success(f"Compra de R${c['compra_total']} do cliente {c['nome']} foi APROVADA.")
            else:
                st.warning("Nenhuma compra acima de R$ 5.000 encontrada.")

    with col2:
        if st.button(" Aprovar Descontos >= 15%"):
            descontos = [c for c in st.session_state.clientes if c.get('desconto', 0) >= 15]
            if descontos:
                for c in descontos:
                    st.success(f"Desconto de {c['desconto']}% para o cliente {c['nome']} foi APROVADO.")
            else:
                st.warning("Nenhum desconto elegível encontrado.")

    with col3:
        if st.button("  Exibir Relatório de Faturamento"):
            total_faturamento = sum(c.get('compra_total', 0) for c in st.session_state.clientes)
            clientes_ativos = [c for c in st.session_state.clientes if c.get('ativo', True)]
            inativos = len(st.session_state.clientes) - len(clientes_ativos)

            st.write(f" Faturamento total: R${total_faturamento}")
            st.write(f" Clientes ativos: {len(clientes_ativos)}")
            st.write(f" Clientes inativos: {inativos}")


            dados_grafico = {
                "Categoria": ["Ativos", "Inativos"],
                "Quantidade": [len(clientes_ativos), inativos]
            }
            st.bar_chart(dados_grafico)

    with col4:
        if st.button("  Manage employees"):
            promovidos = []
            for f in st.session_state.funcionarios:
                if f.get('vendas', 0) > 10 or f.get('entregas', 0) > 20:
                    f['promovido'] = True
                    promovidos.append(f['nome'])
                else:
                    f['promovido'] = False
            if promovidos:
                st.success(f"AUTORIZADO: Funcionários promovidos -> {', '.join(promovidos)}")
            else:
                st.warning("Nenhum funcionário promovido.")
                
    with col5:
        if st.button(" Painel de Controle"):
            st.write("### Dashboard do Sistema")
            dados_dashboard = {
                "Clientes": len(st.session_state.clientes),
                "Produtos": len(st.session_state.produtos),
                "Funcionários": len(st.session_state.funcionarios),
                "Entregas": len(st.session_state.entregas),
                "Estoque": len(st.session_state.estoque)
            }
            st.bar_chart(dados_dashboard)
            
#fast navigation
    st.write("---")
    st.subheader("Navegação Rápida")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button(" Estoque"):
            st.session_state["nav"] = "estoque"
    with col2:
        if st.button(" Clientes"):
            st.session_state["nav"] = "clientes"
    with col3:
        if st.button(" Employees"):
            st.session_state["nav"] = "funcionarios"
    with col4:
        if st.button(" Entregas"):
            st.session_state["nav"] = "entregas"

#exibição
    if st.session_state.get("nav") == "estoque":
        st.write("###  Estoque")
        st.write(st.session_state.estoque)
    elif st.session_state.get("nav") == "clientes":
        st.write("###  Clientes")
        st.write(st.session_state.clientes)
    elif st.session_state.get("nav") == "funcionarios":
        st.write("###   Funcionários")
        st.write(st.session_state.funcionarios)
    elif st.session_state.get("nav") == "entregas":
        st.write("###   Entregas")
        st.write(st.session_state.entregas)
#!--------------------------------------------------------------------------------
        
#! ===== MENU FINAL E PRICNIPAL ====

if menu == "Início":
    start_page()
elif menu == "Área do Cliente":
    client_page()
elif menu == "Área de Produtos":
    product_page()
elif menu == "Área de Estoque":
    stock_page()
elif menu == "Ver Pedidos":
    orders_page()
elif menu == "Gerência Geral":
    management_page()

    


    
