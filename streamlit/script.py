import streamlit as st
from datetime import date
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from project.models.client import Client
from project.models.pallet import Pallet
from project.abstracts.loyalty_system import LoyaltySystem
from project.models.mannager import Manager

# Inicialização do estado da sessão
for key in ["estoque", "produtos", "reservas", "clientes", "funcionarios", "entregas"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "responsavel_estoque" not in st.session_state:
    st.session_state.responsavel_estoque = "João Silva" 
    
if "capacidade_total" not in st.session_state:
    st.session_state.capacidade_total = 10
    
manager = Manager("Demetrios Coutinho", 562662)

st.set_page_config(
    page_title="SISTEMA DE GESTÃO COMERCIAL E LOGÍSTICA DE DISTRIBUIDORA",
    layout="wide"
)

# Menu lateral principal
st.sidebar.markdown("## Menu Principal") 
menu = st.sidebar.radio(
    "Escolha uma seção:",
    [ 
        "Tela Inicial", 
        "Área do Cliente", 
        "Área de Produtos", 
        "Área de Estoque", 
        "Ver Pedidos", 
        "Gerência Geral" 
    ]
) 

# ================= PÁGINAS =================

def start_page():
    st.title("🚀 Bem-vindo ao Sistema de Gestão da Distribuidora")
    st.markdown("---")

    # Mensagem de boas-vindas personalizada
    st.subheader("👋 Olá, seja bem-vindo!")
    st.write("Este é o painel inicial do sistema. Aqui você pode navegar rapidamente para qualquer área e visualizar um resumo da operação.")

    # Atalhos principais
    st.subheader(" Fast Acess")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Ir Para Área do Cliente"):
            st.session_state["nav"] = "cliente"
            client_page()
    with col2:
        if st.button("Ir Para Estoque"):
            st.session_state["nav"] = "estoque"
            stock_page()
    with col3:
        if st.button("Ir Para Pedidos"):
            st.session_state["nav"] = "pedidos"
            orders_page()

    st.markdown("---")

    # Resumo geral do sistema
    st.subheader("  Resumo da Operação")
    dados_dashboard = {
        "Clientes": len(st.session_state.clientes),
        "Produtos": len(st.session_state.produtos),
        "Funcionários": len(st.session_state.funcionarios),
        "Entregas": len(st.session_state.entregas),
        "Estoque": len(st.session_state.estoque)
    }
    st.bar_chart(dados_dashboard)

    st.markdown("---")

    # Interatividade com o usuário
    st.subheader(" Interaja com o nosso Sistema")
    nome_usuario = st.text_input("Digite seu nome:")
    humor = st.selectbox(f"Olá! {nome_usuario} Como você está se sentindo hoje?", [" Ótimo", "Muito Bem", "Estou Neutro", "Muito Cansado"])
    if st.button("Enviar"):
        st.success(f"Olá {nome_usuario}, que bom ter você aqui! Vejo que está se sentindo {humor}. Vamos tornar sua experiência ainda mais produtiva!")

    st.markdown("---")

    # Mensagem motivacional dinâmica
    st.subheader(" Dica do Dia")
    dicas = [
        "Organize seus pedidos logo cedo para evitar atrasos.",
        "Verifique promoções ativas para aumentar suas vendas.",
        "Mantenha o estoque atualizado para evitar rupturas.",
        "Clientes satisfeitos são a chave para o sucesso!"
    ]
    import random
    st.info(random.choice(dicas))


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

    # Comprar produtos
    with st.form("comprar_produto"):
        produto = st.text_input("Pallet do produto que deseja comprar")
        submitted = st.form_submit_button("Efetuar Compra")
    if submitted:
        if produto in st.session_state.produtos:
            client.buy(produto)
            st.success(f"Compra de '{produto}' realizada com sucesso!")
        else:
            st.error("Produto não foi encontrado")

    # Desconto por volume
    with st.form("desconto_volume"):
        quantity_pallets = st.number_input("Quantidade de pallets", min_value=1)
        submitted = st.form_submit_button("Aplicar desconto")
    if submitted and client.volume_discount(quantity_pallets):
        st.success("Desconto aplicado com sucesso!")

    # Pontos fidelidade
    with st.form("pontos_fidelidade"):
        buy_value = st.number_input("Valor da compra", min_value=0.0)
        submitted = st.form_submit_button("Adicionar pontos")
    if submitted and client.add_loyalty_points(buy_value):
        st.success("Pontos adicionados com sucesso!")

    # Reivindicar pontos
    if st.button("🎁 Reivindicar Pontos") and client.claim_points():
        st.success("Pontos resgatados com sucesso!") 

    # Checar promoções
    if st.button("🔍 Ver Promoções"):
        valor = st.number_input("Valor da compra:")
        if client.check_promotion(buy_value=valor):
            st.success("Promoção verificada com sucesso!")

    # Avaliar serviço
    with st.form("avaliacao_servico"):
        rating = st.number_input("Avaliação (1 a 5)", 1, 5)
        comment = st.text_area("Comentário")
        submitted = st.form_submit_button("Enviar avaliação")
    if submitted and client.evaluate_service(rating, comment):
        st.success("Avaliação enviada com sucesso!")
        
#==== PAGINA DE PRODUTOS =========
def product_page():
    st.title("🛒 Gestão de Produtos")
    st.markdown("---")

    # Mostrar todos os pallets disponíveis
    st.subheader("📦 Paletes Disponíveis")
    if st.session_state.produtos:
        for p in st.session_state.produtos:
            st.info(
                f"**Produto:** {p['nome']} | "
                f"**Quantidade:** {p['quantidade']} | "
                f"**Preço Unitário:** R${p['preco']:.2f} | "
                f"**Status:** {p.get('status', 'Ativo')}"
            )
    else:
        st.warning("Nenhum produto cadastrado no estoque.")

    st.markdown("---")

    # Aplicar preço promocional automático
    st.subheader("💰 Preço Promocional Automático")
    if st.button("Aplicar Promoção (10% OFF)"):
        for p in st.session_state.produtos:
            p["preco_promocional"] = round(p["preco"] * 0.9, 2)
        st.success("Preço promocional aplicado em todos os produtos!")

    st.markdown("---")

    # Adição e remoção de paletes
    st.subheader("➕➖ Adição/Remoção de Paletes")
    if st.session_state.produtos:
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
    else:
        st.warning("Nenhum produto disponível para gerenciar.")

    st.markdown("---")

    # Reserva de paletes
    st.subheader("📑 Reserva de Paletes (Compra por Encomenda)")
    if st.session_state.produtos:
        with st.form("form_reserva"):
            cliente_nome = st.text_input("Nome do Cliente")
            cliente_email = st.text_input("Email do Cliente")
            produto_reserva = st.selectbox("Produto para reserva:", [p["nome"] for p in st.session_state.produtos])
            qtd_reserva = st.number_input("Quantidade de paletes para reserva", min_value=1, step=1)
            reservar = st.form_submit_button("Reservar")

            if reservar:
                st.success(f"Reserva feita para {cliente_nome}: {qtd_reserva} paletes de {produto_reserva}.")
    else:
        st.warning("Nenhum produto disponível para reserva.")

    st.markdown("---")

    # Promoções
    st.subheader("🎯 Promoções")
    if st.session_state.produtos:
        produto_promocao = st.selectbox("Selecione o produto:", [p["nome"] for p in st.session_state.produtos])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Verificar Promoção"):
                for p in st.session_state.produtos:
                    if p["nome"] == produto_promocao:
                        if "preco_promocional" in p:
                            st.success(f"Preço promocional aplicado: R${p['preco_promocional']:.2f}")
                        else:
                            st.warning("Nenhum preço promocional aplicado.")
        with col2:
            if st.button("Remover Promoção"):
                for p in st.session_state.produtos:
                    if p["nome"] == produto_promocao and "preco_promocional" in p:
                        del p["preco_promocional"]
                        st.info("Promoção removida com sucesso.")
    else:
        st.warning("Nenhum produto disponível para promoções.")

    st.markdown("---")

    # Sumário geral do produto
    st.subheader("📊 Sumário Geral do Produto")
    if st.session_state.produtos:
        produto_info = st.selectbox("Selecione o produto:", [p["nome"] for p in st.session_state.produtos])
        if st.button("Mostrar Informações"):
            for p in st.session_state.produtos:
                if p["nome"] == produto_info:
                    st.write(f"**Nome:** {p['nome']}")
                    st.write(f"**Quantidade:** {p['quantidade']}")
                    st.write(f"**Preço Unitário:** R${p['preco']:.2f}")
                    st.write(f"**Preço Promocional:** {p.get('preco_promocional', 'Sem promoção')}")
                    st.write(f"**Marca:** {p.get('marca', 'Não informado')}")
                    st.write(f"**Categoria:** {p.get('categoria', 'Não informado')}")
                    st.write(f"**Fornecedor:** {p.get('fornecedor', 'Não informado')}")
                    st.write(f"**Origem:** {p.get('origem', 'Não informado')}")
                    st.write(f"**Código de Barras:** {p.get('codigo_barras', 'Não informado')}")
                    st.write(f"**Validade:** {p.get('validade', 'Não informado')}")
                    st.write(f"**Status:** {p.get('status', 'Ativo')}")
    else:
        st.warning("Nenhum produto cadastrado.")

    st.markdown("---")

    # Gráfico comparativo
    st.subheader("📈 Comparativo de Paletes por Produto")
    if st.session_state.produtos:
        dados = {
            "Produto": [p["nome"] for p in st.session_state.produtos],
            "Quantidade": [p["quantidade"] for p in st.session_state.produtos]
        }
        st.bar_chart(dados)
    else:
        st.warning("Nenhum produto cadastrado para gerar gráfico.")
        
        

def stock_page():
    st.title("📦 Gestão de Estoque")
    st.markdown("---")

    # Adicionar paletes ao estoque
    st.subheader("➕ Adicionar Paletes")
    with st.form("form_add_pallet"):
        nome = st.text_input("Nome do Produto/Pallet") 
        quantidade = st.number_input("Quantidade", min_value=1, step=1) 
        preco_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, step=0.01) 
        marca = st.text_input("Marca")
        categoria = st.text_input("Categoria")
        fornecedor = st.text_input("Fornecedor")
        validade = st.date_input("Data de Validade")
        is_active = st.checkbox("Produto ativo (não vencido)?", value=True) 
        submitted = st.form_submit_button("Adicionar ao Estoque")

        if submitted:
            if is_active:
                novo_produto = {
                    "nome": nome,
                    "quantidade": quantidade,
                    "preco": preco_unitario,
                    "marca": marca,
                    "categoria": categoria,
                    "fornecedor": fornecedor,
                    "validade": validade,
                    "status": "Ativo" if is_active else "Inativo"
                }
                st.session_state.estoque.append(novo_produto)
                st.session_state.produtos.append(novo_produto)  # 🔗 integração com gestão de produtos
                st.success(f"{quantidade} paletes de {nome} adicionados ao estoque e vinculados à gestão de produtos.")
            else:
                st.error(f"O pallet '{nome}' está vencido e não pode ser adicionado.")

    st.markdown("---")

    # Remover paletes
    st.subheader("➖ Remover Paletes")
    if st.session_state.estoque:
        produto_remover = st.selectbox("Selecione o produto para remover:", [p["nome"] for p in st.session_state.estoque])
        qtd_remover = st.number_input("Quantidade a remover", min_value=1, step=1)
        confirmar = st.checkbox("Confirmar remoção do produto selecionado")
        if st.button("Remover"):
            for p in st.session_state.estoque:
                if p["nome"] == produto_remover:
                    if p["quantidade"] >= qtd_remover and confirmar:
                        p["quantidade"] -= qtd_remover
                        st.success(f"{qtd_remover} paletes de {produto_remover} removidos do estoque.")
                        # Atualiza também na aba de produtos
                        for prod in st.session_state.produtos:
                            if prod["nome"] == produto_remover:
                                prod["quantidade"] = p["quantidade"]
                    else:
                        st.error("Quantidade insuficiente ou remoção não confirmada.")
    else:
        st.warning("Estoque vazio. Nenhum pallet para remover.")

    st.markdown("---")

    # Listar paletes e valor total
    st.subheader("📑 Listagem de Paletes e Valor Total")
    if st.button("Listar Paletes"):
        if st.session_state.estoque:
            valor_total = sum(p["preco"] * p["quantidade"] for p in st.session_state.estoque)
            for p in st.session_state.estoque:
                st.info(
                    f"**Produto:** {p['nome']} | "
                    f"**Quantidade:** {p['quantidade']} | "
                    f"**Preço Unitário:** R${p['preco']:.2f} | "
                    f"**Marca:** {p.get('marca', 'Não informado')} | "
                    f"**Categoria:** {p.get('categoria', 'Não informado')} | "
                    f"**Fornecedor:** {p.get('fornecedor', 'Não informado')} | "
                    f"**Validade:** {p.get('validade', 'Não informado')} | "
                    f"**Status:** {p.get('status', 'Ativo')}"
                )
            st.success(f"💰 Valor total do estoque: R${valor_total:.2f}")
            st.info(f"📦 Total de pallets: {sum(p['quantidade'] for p in st.session_state.estoque)}")
        else:
            st.warning("Estoque vazio.")

    st.markdown("---")

    # Informações gerais do estoque
    st.subheader("📊 Informações Gerais do Estoque")
    if st.button("Mostrar Informações"):
        if st.session_state.estoque:
            valor_total = sum(p["preco"] * p["quantidade"] for p in st.session_state.estoque)
            quantidade_total = sum(p["quantidade"] for p in st.session_state.estoque)
            capacidade_total = st.session_state.capacidade_total

            st.write(f"**Responsável pelo Estoque:** {st.session_state.responsavel_estoque}")
            st.write(f"**Capacidade Máxima:** {capacidade_total} pallets")
            st.write(f"**Ocupação Atual:** {quantidade_total}/{capacidade_total} pallets")

            ocupacao = quantidade_total / capacidade_total
            st.progress(min(ocupacao, 1.0))

            dados = {
                "Métrica": ["Valor Total (R$)", "Quantidade Total"],
                "Valor": [valor_total, quantidade_total]
            }
            st.bar_chart(dados, x="Métrica", y="Valor")
        else:
            st.warning("Estoque vazio.")

    # (mantive sua lógica original, apenas organizada)

def orders_page():
    st.title("📑 Gestão de Pedidos")
    st.markdown("---")
    st.write("Área dedicada ao registro, acompanhamento e análise de pedidos dos clientes.")

    # Criar novo pedido
    st.subheader("🆕 Criar Novo Pedido")
    with st.form("form_pedido"):
        cliente_nome = st.text_input("Nome do Cliente")
        produto = st.selectbox("Produto", [p["nome"] for p in st.session_state.produtos]) if st.session_state.produtos else st.text_input("Produto")
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        status = st.selectbox("Status do Pedido", ["Pendente", "Em Processamento", "Concluído", "Cancelado"])
        submitted = st.form_submit_button("Registrar Pedido")

        if submitted:
            novo_pedido = {
                "cliente": cliente_nome,
                "produto": produto,
                "quantidade": quantidade,
                "status": status,
                "valor_total": None
            }
            # Calcula valor total se produto existe
            for p in st.session_state.produtos:
                if p["nome"] == produto:
                    novo_pedido["valor_total"] = quantidade * p["preco"]
            st.session_state.reservas.append(novo_pedido)
            st.success(f"Pedido registrado para {cliente_nome}: {quantidade}x {produto} (Status: {status})")

    st.markdown("---")

    # Listar pedidos
    st.subheader("📋 Lista de Pedidos")
    if st.session_state.reservas:
        for i, pedido in enumerate(st.session_state.reservas, start=1):
            st.info(
                f"**Pedido {i}:** Cliente: {pedido['cliente']} | "
                f"Produto: {pedido['produto']} | "
                f"Quantidade: {pedido['quantidade']} | "
                f"Status: {pedido['status']} | "
                f"Valor Total: R${pedido['valor_total']:.2f}" if pedido['valor_total'] else "Valor não calculado"
            )
    else:
        st.warning("Nenhum pedido registrado até o momento.")

    st.markdown("---")

    # Atualizar status de pedidos
    st.subheader("🔄 Atualizar Status de Pedido")
    if st.session_state.reservas:
        pedido_selecionado = st.selectbox("Selecione o pedido:", [f"{i+1} - {p['cliente']} ({p['produto']})" for i, p in enumerate(st.session_state.reservas)])
        novo_status = st.selectbox("Novo Status:", ["Pendente", "Em Processamento", "Concluído", "Cancelado"])
        if st.button("Atualizar Status"):
            idx = int(pedido_selecionado.split(" - ")[0]) - 1
            st.session_state.reservas[idx]["status"] = novo_status
            st.success(f"Status do pedido {pedido_selecionado} atualizado para {novo_status}.")
    else:
        st.warning("Nenhum pedido disponível para atualização.")

    st.markdown("---")

    # Relatório de pedidos
    st.subheader("📊 Relatório de Pedidos")
    if st.button("Gerar Relatório"):
        if st.session_state.reservas:
            total_pedidos = len(st.session_state.reservas)
            concluidos = sum(1 for p in st.session_state.reservas if p["status"] == "Concluído")
            pendentes = sum(1 for p in st.session_state.reservas if p["status"] == "Pendente")
            cancelados = sum(1 for p in st.session_state.reservas if p["status"] == "Cancelado")
            valor_total = sum(p["valor_total"] for p in st.session_state.reservas if p["valor_total"])

            st.info(f"📦 Total de pedidos: {total_pedidos}")
            st.info(f"✅ Concluídos: {concluidos}")
            st.info(f"⏳ Pendentes: {pendentes}")
            st.info(f"❌ Cancelados: {cancelados}")
            st.info(f"💰 Valor total em pedidos: R${valor_total:.2f}")

            dados_relatorio = {
                "Status": ["Concluídos", "Pendentes", "Cancelados"],
                "Quantidade": [concluidos, pendentes, cancelados]
            }
            st.bar_chart(dados_relatorio)
        else:
            st.warning("Nenhum pedido registrado para gerar relatório.")




def management_page():
    st.title("👨‍💼 Gerência Geral")
    st.markdown("---")
    st.write("Área dedicada ao gerenciamento de compras, descontos, funcionários e relatórios estratégicos.")

    # Painel de ações rápidas
    st.subheader("⚡ Ações Rápidas")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Aprovar Compras +R$ 5.000"):
            aprovadas = [c for c in st.session_state.clientes if c.get('compra_total', 0) >= 5000]
            if aprovadas:
                for c in aprovadas:
                    st.success(f"Compra de R${c['compra_total']:.2f} do cliente {c['nome']} foi APROVADA.")
            else:
                st.warning("Nenhuma compra acima de R$ 5.000 encontrada.")

    with col2:
        if st.button("💸 Aprovar Descontos >= 15%"):
            descontos = [c for c in st.session_state.clientes if c.get('desconto', 0) >= 15]
            if descontos:
                for c in descontos:
                    st.success(f"Desconto de {c['desconto']}% para o cliente {c['nome']} foi APROVADO.")
            else:
                st.warning("Nenhum desconto elegível encontrado.")

    with col3:
        if st.button("📊 Relatório de Faturamento"):
            total_faturamento = sum(c.get('compra_total', 0) for c in st.session_state.clientes)
            clientes_ativos = [c for c in st.session_state.clientes if c.get('ativo', True)]
            inativos = len(st.session_state.clientes) - len(clientes_ativos)

            st.info(f"💰 Faturamento total: R${total_faturamento:.2f}")
            st.info(f"👥 Clientes ativos: {len(clientes_ativos)}")
            st.info(f"🚫 Clientes inativos: {inativos}")

            dados_grafico = {
                "Categoria": ["Ativos", "Inativos"],
                "Quantidade": [len(clientes_ativos), inativos]
            }
            st.bar_chart(dados_grafico)

    st.markdown("---")

    # Gestão de funcionários
    st.subheader("👔 Gestão de Funcionários")
    if st.button("📈 Avaliar Performance"):
        promovidos = []
        for f in st.session_state.funcionarios:
            if f.get('vendas', 0) > 10 or f.get('entregas', 0) > 20:
                f['promovido'] = True
                promovidos.append(f['nome'])
            else:
                f['promovido'] = False
        if promovidos:
            st.success(f"Funcionários promovidos: {', '.join(promovidos)}")
        else:
            st.warning("Nenhum funcionário elegível para promoção.")

    st.markdown("---")

    # Dashboard geral
    st.subheader("📊 Dashboard do Sistema")
    if st.button("📌 Exibir Painel"):
        dados_dashboard = {
            "Clientes": len(st.session_state.clientes),
            "Produtos": len(st.session_state.produtos),
            "Funcionários": len(st.session_state.funcionarios),
            "Entregas": len(st.session_state.entregas),
            "Estoque": len(st.session_state.estoque)
        }
        st.bar_chart(dados_dashboard)

    st.markdown("---")

    # Navegação rápida
    st.subheader("🚀 Navegação Rápida")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📦 Estoque"):
            st.write(st.session_state.estoque)
    with col2:
        if st.button("👥 Clientes"):
            st.write(st.session_state.clientes)
    with col3:
        if st.button("👔 Funcionários"):
            st.write(st.session_state.funcionarios)
    with col4:
        if st.button("🚚 Entregas"):
            st.write(st.session_state.entregas)


# ================= NAVEGAÇÃO PRINCIPAL =================

if menu == "Tela Inicial":
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
