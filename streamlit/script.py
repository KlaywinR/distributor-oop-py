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


#! sessões de estado.

for key in ["estoque", "produtos", "reservas", "clientes", "funcionarios", "entregas"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "responsavel_estoque" not in st.session_state:
    st.session_state.responsavel_estoque = "João Silva" 
    
if "capacidade_total" not in st.session_state:
    st.session_state.capacidade_total = 10

if "stock_obj" not in st.session_state:
    st.session_state.stock_obj = Stock(10, "João Silva", "Estoque Central")

manager = Manager("Demetrios Coutinho", 562662)

st.set_page_config(
    page_title="SISTEMA DE GESTÃO COMERCIAL E LOGÍSTICA DE DISTRIBUIDORA",
    layout="wide"
)


st.sidebar.markdown("## Menu Principal") 
menu = st.sidebar.radio(
    "Choose a session:",
    [ 
        "Tela Inicial", 
        "Área Cliente", 
        "Área Produtos", 
        "Área Estoque", 
        "Área Pedidos", 
        "Área Gerente",
        "Área Vendedor",
        "Área Motorista",
        "Área de Entregas"
    ]
) 

# === Páginas ===
def start_page():
    st.title("Sistema DistriSys")
    st.markdown("---")

    st.subheader("Olá, seja bem-vindo!")
    st.write("Este é o painel inicial do sistema. Você pode navegar rapidamente para qualquer área e visualizar um resumo de operações.")

    st.subheader(" Fast Acess")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Ir Para Área do Cliente"):
            st.session_state["nav"] = "cliente"
            client_page()
    with col2:
<<<<<<< Updated upstream
        if st.button("Ir Para Estoque"):
            st.session_state["nav"] = "estoque"
            stock_page()
    with col3:
        if st.button("Ir Para Pedidos"):
            st.session_state["nav"] = "pedidos"
            orders_page()
            
    st.markdown("---")

    st.subheader("Summary")
    dados_dashboard = {
        "Clientes": len(st.session_state.clientes),
        "Produtos": len(st.session_state.produtos),
        "Funcionários": len(st.session_state.funcionarios),
        "Entregas": len(st.session_state.entregas),
        "Estoque": len(st.session_state.estoque)
    }
    st.bar_chart(dados_dashboard)

    st.markdown("---")

    st.subheader(" Interaja com o nosso Sistema")
    username = st.text_input("Digite seu nome:")
    humor = st.selectbox(f"Olá! {username} Como você está se sentindo hoje?", [" Ótimo", "Muito Bem", "Estou Neutro", "Muito Cansado"])
    if st.button("Enter"):
        st.success(f"Olá {username}, que bom ter você aqui! Vejo que está se sentindo {humor}. Vamos tornar sua experiência ainda mais produtiva!")

    st.markdown("---")

    st.subheader(" Dica do Dia")
    tip = [
        "Organize seus pedidos logo cedo para evitar atrasos.",
        "Verifique promoções ativas para aumentar suas vendas.",
        "Mantenha o estoque atualizado para evitar rupturas.",
        "Clientes satisfeitos são a chave para o sucesso!"
    ]
    import random
    st.info(random.choice(tip))

#=== Página do Cliente ===
def client_page():
    st.subheader("Clients")
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
    
    #Formulárioa de interação do cliente
    with st.form("comprar_produto"):# formulário de compra de produto por parte do cliente.
        produto = st.text_input("Nome do produto que deseja comprar")
        submitted = st.form_submit_button("Efetuar Compra")
    if submitted:
        if produto in st.session_state.produtos:
            client.buy(produto)
            st.success(f"Compra de '{produto}' realizada com sucesso!")
        else:
            st.error("Produto não foi encontrado")

    with st.form("desconto_volume"):#Desconto acerca do volume da compra do cliente.
        quantity_pallets = st.number_input("Quantidade de pallets", min_value=1)
        submitted = st.form_submit_button("Aplicar desconto")
    if submitted and client.volume_discount(quantity_pallets):
        st.success("Desconto aplicado com sucesso!")


    with st.form("pontos_fidelidade"):#Adicionar pontos fidelidade a compra do cliente
        buy_value = st.number_input("Valor da compra", min_value=0.0)
        submitted = st.form_submit_button("Adicionar pontos")
    if submitted and client.add_loyalty_points(buy_value):
        st.success("Pontos adicionados com sucesso!")

    if st.button("Desejo Reivindicar Pontos") and client.claim_points():#Cliente resgata pontos acumulados
        st.success("Pontos resgatados com sucesso!") 

    if st.button("Desejo Ver Promoções"):#Cliente verifica promoções aplicadas
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
        
#=== Página de Produtos ===
def product_page():
    st.title("Gestão de Produtos")
    st.markdown("---")
=======
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
>>>>>>> Stashed changes

    st.subheader("Paletes Disponíveis")
    if st.session_state.produtos:
        for p in st.session_state.produtos:
            st.info(
                f"**Produto:** {p['nome']} | "
                f"**Quantidade:** {p['quantidade']} | "
                f"**Preço Unitário:** R${p['preco']:.2f} | "
                f"**Status:** {p.get('status', 'Ativo')}"
            )
    else:
        st.warning("Mensagem do Sistem: Nenhum produto cadastrado no estoque.")

    st.markdown("---")

    st.subheader("Preço Promocional Automático")
    if st.button("Aplicar Promoção - 10% OFF"):
        for p in st.session_state.produtos:
            p["preco_promocional"] = round(p["preco"] * 0.9, 2)
        st.success("O Preço promocional foi aplicado em todos os produtos!")

    st.markdown("---")

    st.subheader("Adição ou Remoção de Pallets")
    if st.session_state.produtos:
        produto_selecionado = st.selectbox("Por favor, selecione o produto:", [p["nome"] for p in st.session_state.produtos])
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
        st.warning("Mensagem do sistema: Nenhum produto disponível para gerenciar.")

    st.markdown("---")

    st.subheader("Reserva de Pallets - Compras por Encomenda")
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
        st.warning("Mensagem do Sistema: Nenhum produto disponível para reserva.")

    st.markdown("---")

    st.subheader("Promoções")
    if st.session_state.produtos:
        produto_promocao = st.selectbox("Selecione o produto:", [p["nome"] for p in st.session_state.produtos])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Desejo Verificar Promoção"):
                for p in st.session_state.produtos:
                    if p["nome"] == produto_promocao:
                        if "preco_promocional" in p:
                            st.success(f"Preço promocional aplicado: R${p['preco_promocional']:.2f}")
                        else:
                            st.warning("Mensagem do Sistema: Nenhum preço promocional aplicado.")
        with col2:
            if st.button("Remover Promoção"):
                for p in st.session_state.produtos:
                    if p["nome"] == produto_promocao and "preco_promocional" in p:
                        del p["preco_promocional"]
                        st.info("Promoção removida com sucesso.")
    else:
        st.warning("Mensagem do Sistema: Nenhum produto disponível para promoções.")

    st.markdown("---")

    st.subheader("Sumário Geral do Produto")
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
        st.warning("Mensagem do Sistema: Nenhum produto cadastrado.")

    st.markdown("---")

    st.subheader("Comparativo de Pallets por Produto")
    if st.session_state.produtos:
        dados = {
            "Produto": [p["nome"] for p in st.session_state.produtos],
            "Quantidade": [p["quantidade"] for p in st.session_state.produtos]
        }
        st.bar_chart(dados)
    else:
        st.warning("Mensagem do Sistema: Nenhum produto foi cadastrado para geração do gráfico.")
        
        
#=== Página do Estoque ===
def stock_page():
    st.title("   Gestão de Estoque")
    st.markdown("---")

    stock = st.session_state.stock_obj

    st.subheader("  Adicionar Paletes")
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
                try:
                    # Criar objeto Product
                    produto_obj = Product(
                        name=nome,
                        category=categoria,
                        unit_measure="UN",
                        brand=marca,
                        wheight_per_unit=1.0,
                        pallets_quantity=int(quantidade),
                        barcode=f"BAR_{nome}_{fornecedor}",
                        total_units=int(quantidade),
                        cost_price=preco_unitario,
                        quantity=int(quantidade),
                        supplier=fornecedor,
                        min_stock=1,
                        origin="Distribuidor",
                        units_per_pallet=1,
                        min_pallets=1,
                        unit_price=preco_unitario,
                        expiration_date=validade
                    )
                    
                    # Adicionar ao Stock
                    stock.add_pallet(produto_obj, int(quantidade))
                    
                    # Manter também no session_state para compatibilidade
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
                    st.session_state.produtos.append(novo_produto)  
                    st.success(f"{quantidade} paletes de {nome} adicionados ao estoque e vinculados à gestão de produtos.")
                except Exception as e:
                    st.error(f"Erro ao adicionar produto: {str(e)}")
            else:
                st.error(f"O pallet '{nome}' está vencido e não pode ser adicionado.")

    st.markdown("---")

    st.subheader("   Remover Paletes")
    if st.session_state.estoque:
        produto_remover = st.selectbox("Selecione o produto para remover:", [p["nome"] for p in st.session_state.estoque])
        qtd_remover = st.number_input("Quantidade a remover", min_value=1, step=1)
        confirmar = st.checkbox("Confirmar remoção do produto selecionado")
        if st.button("Remover"):
            produto_encontrado_estoque = None
            for p in st.session_state.estoque:
                if p["nome"] == produto_remover:
                    produto_encontrado_estoque = p
                    break
            
            if produto_encontrado_estoque:
                if produto_encontrado_estoque["quantidade"] >= qtd_remover and confirmar:
                    try:
                        # Encontrar o produto correspondente no estoque
                        produto_encontrado = None
                        for item in stock.list_pallets():
                            if item.product.name == produto_remover:
                                produto_encontrado = item.product
                                break
                        
                        if produto_encontrado:
                            # Chamar del_pallet com o objeto Product correto
                            stock.del_pallet(produto_encontrado, qtd_remover)
                            produto_encontrado_estoque["quantidade"] -= qtd_remover
                            
                            # Se a quantidade chegou a 0, remove o produto do estoque
                            if produto_encontrado_estoque["quantidade"] == 0:
                                st.session_state.estoque.remove(produto_encontrado_estoque)
                               
                            # Sincronizar com produtos também
                            for prod in st.session_state.produtos:
                                if prod["nome"] == produto_remover:
                                    prod["quantidade"] = produto_encontrado_estoque["quantidade"]
                                    if prod["quantidade"] == 0:
                                        st.session_state.produtos.remove(prod)
                            
                            st.success(f"{qtd_remover} paletes de {produto_remover} removidos do estoque.")
                        else:
                            st.error(f"Produto '{produto_remover}' não encontrado no estoque de objetos.")
                    except ValueError as e:
                        st.error(f"Erro ao remover: {str(e)}")
                else:
                    st.error("Quantidade insuficiente ou remoção não confirmada.")
    else:
        st.warning("Mensagem do Sistema: Estoque vazio. Nenhum pallet para remover.")

    st.markdown("---")

  
    st.subheader("   Listagem de Paletes e Valor Total")
    if st.button("Listar Paletes"):
        # Sincronizar com o Stock para pegar dados atualizados
        estoque_atualizado = []
        for item in stock.list_pallets():
            estoque_atualizado.append({
                "nome": item.product._name,
                "quantidade": item.pallets,
                "preco": item.product.current_price(),
                "marca": item.product._brand,
                "categoria": item.product._category,
                "fornecedor": item.product._supplier,
                "validade": item.product._expiration_date,
                "status": "Ativo" if item.product.is_active() else "Inativo"
            })
        
        if estoque_atualizado:
            valor_total = sum(p["preco"] * p["quantidade"] for p in estoque_atualizado)
            for p in estoque_atualizado:
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
            st.success(f"    Valor total do estoque: R${valor_total:.2f}")
            st.info(f"   Total de pallets: {sum(p['quantidade'] for p in estoque_atualizado)}")
        else:
            st.warning("Estoque vazio.")

    st.markdown("---")

    st.subheader("   Informações Gerais do Estoque")
    if st.button("Quero Mostrar Informações"):
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
            
#=== Página de Pedidos ===
def orders_page():
    st.title("   Gestão de Pedidos")
    st.markdown("---")
    st.write("Esta Área é dedicada ao registro, acompanhamento e análise de pedidos dos clientes.")

    st.subheader("   Criar Novo Pedido")
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
            
            for p in st.session_state.produtos:
                if p["nome"] == produto:
                    novo_pedido["valor_total"] = quantidade * p["preco"]
            st.session_state.reservas.append(novo_pedido)
            st.success(f"Pedido registrado para {cliente_nome}: {quantidade}x {produto} (Status: {status})")

    st.markdown("---")

    st.subheader("   Lista de Pedidos")
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
        st.warning("Mensagem do Sistema: Nenhum pedido registrado até o momento.")

    st.markdown("---")

    st.subheader("   Atualizar Status de Pedido")
    if st.session_state.reservas:
        pedido_selecionado = st.selectbox("Selecione o pedido:", [f"{i+1} - {p['cliente']} ({p['produto']})" for i, p in enumerate(st.session_state.reservas)])
        novo_status = st.selectbox("Novo Status:", ["Pendente", "Em Processamento", "Concluído", "Cancelado"])
        if st.button("Atualizar Status"):
            idx = int(pedido_selecionado.split(" - ")[0]) - 1
            st.session_state.reservas[idx]["status"] = novo_status
            st.success(f"Status do pedido {pedido_selecionado} atualizado para {novo_status}.")
    else:
        st.warning("Mensagem do Sistema: Nenhum pedido disponível para atualização.")
    st.markdown("---")

    st.subheader("   Relatório de Pedidos")
    if st.button("Gerar Relatório"):
        if st.session_state.reservas:
            total_pedidos = len(st.session_state.reservas)
            concluidos = sum(1 for p in st.session_state.reservas if p["status"] == "Concluído")
            pendentes = sum(1 for p in st.session_state.reservas if p["status"] == "Pendente")
            cancelados = sum(1 for p in st.session_state.reservas if p["status"] == "Cancelado")
            valor_total = sum(p["valor_total"] for p in st.session_state.reservas if p["valor_total"])

            st.info(f"   Total de pedidos: {total_pedidos}")
            st.info(f"   Concluídos: {concluidos}")
            st.info(f"   Pendentes: {pendentes}")
            st.info(f"   Cancelados: {cancelados}")
            st.info(f"   Valor total em pedidos: R${valor_total:.2f}")

            dados_relatorio = {
                "Status": ["Concluídos", "Pendentes", "Cancelados"],
                "Quantidade": [concluidos, pendentes, cancelados]
            }
            st.bar_chart(dados_relatorio)
        else:
            st.warning("Mensagem do Sistema: Nenhum pedido registrado para gerar relatório.")

#=== Página de Gerenciamento do Gerente ===
def management_page():
    st.title(" Gerênciamento Geral")
    st.markdown("---")
    st.write("Área dedicada ao gerenciamento de compras, descontos, funcionários e relatórios estratégicos.")

    st.subheader("  Minhas Ações Rápidas")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("  Aprovar Compras +R$ 5.000"):
            aprovadas = [c for c in st.session_state.clientes if c.get('compra_total', 0) >= 5000]
            if aprovadas:
                for c in aprovadas:
                    st.success(f"Compra de R${c['compra_total']:.2f} do cliente {c['nome']} foi APROVADA.")
            else:
                st.warning("Mensagem do Sistema: Nenhuma compra acima de R$ 5.000 encontrada.")

    with col2:
        if st.button("   Aprovar Descontos >= 15%"):
            descontos = [c for c in st.session_state.clientes if c.get('desconto', 0) >= 15]
            if descontos:
                for c in descontos:
                    st.success(f"Desconto de {c['desconto']}% para o cliente {c['nome']} foi APROVADO.")
            else:
                st.warning("Mensagem do Sistema: Nenhum desconto elegível encontrado.")

    with col3:
        if st.button("Exibir Relatório de Faturamento"):
            total_faturamento = sum(c.get('compra_total', 0) for c in st.session_state.clientes)
            clientes_ativos = [c for c in st.session_state.clientes if c.get('ativo', True)]
            inativos = len(st.session_state.clientes) - len(clientes_ativos)

            st.info(f"   Faturamento total: R${total_faturamento:.2f}")
            st.info(f"   Clientes ativos: {len(clientes_ativos)}")
            st.info(f"   Clientes inativos: {inativos}")

            dados_grafico = {
                "Categoria": ["Ativos", "Inativos"],
                "Quantidade": [len(clientes_ativos), inativos]
            }
            st.bar_chart(dados_grafico)

    st.markdown("---")

    st.subheader("   Gestão de Funcionários")
    if st.button("   Avaliar Performance"):
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
            st.warning("Mensagem do Sistema: Nenhum funcionário elegível para promoção.")

    st.markdown("---")

    st.subheader("  Dashboard do Sistema")
    if st.button("  Exibir Painel"):
        dados_dashboard = {
            "Clientes": len(st.session_state.clientes),
            "Produtos": len(st.session_state.produtos),
            "Funcionários": len(st.session_state.funcionarios),
            "Entregas": len(st.session_state.entregas),
            "Estoque": len(st.session_state.estoque)
        }
        st.bar_chart(dados_dashboard)

    st.markdown("---")


    st.subheader(" Minha Navegação Rápida")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("View Stock"):
            menu = "Área Estoque"
            stock_page()
    with col2:
<<<<<<< Updated upstream
        if st.button("View Clients"):
            menu = "Área Cliente"
            client_page()
=======
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
>>>>>>> Stashed changes
    with col3:
        if st.button("View Employees"):
            menu = "Área Funcionários"
            st.write(st.session_state.funcionarios)
    with col4:
        if st.button("View Deliveries"):
            st.write(st.session_state.entregas)

#=== Página do Vendedor  ===
def seller_page():
    st.title(" Área do Vendedor")
    st.markdown("---")
    st.write("Gerencie suas vendas, clientes atendidos, comissões e metas mensais.")


    if "seller" not in st.session_state:
        from datetime import date 
        from project.models.seller import Seller     
        
        st.session_state.seller = Seller(
            name="Carlos Souza",
            shift="Manhã",
            cpf="123.456.789-00",
            salary=3500,
            id_employee=101,
            departament="Vendas",
            status_employee="Ativo",
            admission_date=date.today(),
            contract_type="CLT",
            position="Vendedor",
            meta_monthly=50,
            overtime=5,
            hours_worked=160,
            commision_percentual=10
        )
    seller = st.session_state.seller

    # === Registrar Cliente Atendido ===
    st.subheader(" Registrar Cliente Atendido")
    cliente_nome = st.text_input("Nome do Cliente Atendido")
    if st.button("Registrar Atendimento"):
        seller.attend_costumer(cliente_nome)
        st.success(f"Cliente {cliente_nome} registrado como atendido.")

  
    st.subheader(" Registrar Venda")
    cliente_venda = st.text_input("Cliente da Venda")
    produto_venda = st.text_input("Produto Vendido")
    qtd_venda = st.number_input("Quantidade", min_value=1, step=1)
    if st.button("Registrar Venda"):
        seller.make_sale(cliente_venda, produto_venda, qtd_venda)
        seller.add_pallets_sold(qtd_venda)
        st.success(f"Venda registrada: {qtd_venda}x {produto_venda} para {cliente_venda}")


    st.subheader(" Negociar Preço")
    desconto = st.slider("Selecione o desconto (%)", 0.0, 0.15, 0.05)
    if st.button("Negociar"):
        st.info(seller.negotiate_price(desconto))


    st.subheader(" Responder Reclamação")
    cliente_reclamacao = st.text_input("Cliente com Reclamação")
    if st.button("Responder Reclamação"):
        st.success(seller.respond_to_complaint(cliente_reclamacao))

  
    st.subheader(" Verificar Crédito do Cliente")
    cliente_credito = st.text_input("Nome do Cliente (simulado)")
    if st.button("Verificar Crédito"):
        class FakeClient:
            def __init__(self, name, credit_score):
                self.name = name
                self.credit_score = credit_score
        fake_client = FakeClient(cliente_credito, 650)
        st.info(seller.see_costumer_credit(fake_client))


    st.subheader(" Acompanhamento e Benefícios")
    cliente_acomp = st.text_input("Cliente para acompanhamento")
    if st.button("Fazer Acompanhamento"):
        st.success(seller.follow_costumer(cliente_acomp))
    if st.button("Aplicar Benefício"):
        st.success(seller.apply_costumer_benefi(cliente_acomp))

    st.subheader(" Solicitar Avaliação")
    nota = st.number_input("Nota (1 a 5)", min_value=1, max_value=5, step=1)
    if st.button("Registrar Avaliação"):
        try:
            seller.request_evaluation(nota)
            st.success("Avaliação registrada com sucesso.")
        except ValueError as e:
            st.error(str(e))

    st.subheader(" Sumário de Vendas")
    if st.button("Exibir Sumário"):
        resumo = seller.sumary_sales()
        st.write(resumo)
        st.bar_chart({
            "Métrica": ["Clientes Atendidos", "Vendas Realizadas", "Paletes Vendidos", "Comissão"],
            "Valor": [resumo["clientes_atendidos"], resumo["vendas_realizadas"], resumo["paletes_vendidos"], resumo["comissao"]]
        })

    st.markdown("---")
    st.info(str(seller))

#== Area do Motorista ===
def driver_page():
    st.title("🚚 Área do Motorista")
    st.markdown("---")
    st.write("Gerencie entregas, ocorrências, disponibilidade e status do motorista.")

    # Inicializa um motorista na sessão
    if "driver" not in st.session_state:
        from datetime import date
        from project.models.driver import Driver   
        st.session_state.driver = Driver(
            id_driver=1,
            name="José Ferreira",
            cpf="987.654.321-00",
            cnh_category="D",
            cnh_expiration=date(2027, 5, 20),
            max_capacity_pallets=100,
            region="Nordeste"
        )
    driver = st.session_state.driver

    # === Verificar CNH ===
    st.subheader("📄 Validade da CNH")
    if st.button("Verificar CNH"):
        if driver.cnh_is_valid():
            st.success("CNH válida! ✅")
        else:
            st.error("CNH vencida ❌")

    # === Verificar se pode operar ===
    st.subheader("⚙️ Disponibilidade para Operar")
    if st.button("Verificar Disponibilidade"):
        if driver.can_operate():
            st.success("Motorista pode operar 🚚")
        else:
            st.error("Motorista não pode operar ❌")

    # === Atribuir Entrega ===
    st.subheader("📦 Atribuir Entrega")
    entrega_nome = st.text_input("Nome da Entrega")
    if st.button("Atribuir Entrega"):
        try:
            driver.assign_delivery(entrega_nome)
            st.success(f"Entrega '{entrega_nome}' atribuída ao motorista.")
        except PermissionError as e:
            st.error(str(e))

    # === Rejeitar Entrega ===
    st.subheader("❌ Rejeitar Entrega")
    if st.button("Rejeitar Entrega"):
        driver.reject_delivery()
        st.warning("Entrega rejeitada e ocorrência registrada.")

    # === Registrar Ocorrência ===
    st.subheader("⚠️ Registrar Ocorrência")
    ocorrencia = st.text_input("Descrição da Ocorrência")
    if st.button("Registrar Ocorrência"):
        driver.register_occurance(ocorrencia)
        st.success(f"Ocorrência registrada: {ocorrencia}")

    # === Histórico de Entregas ===
    st.subheader("📊 Histórico de Entregas")
    if st.button("Exibir Histórico"):
        if len(driver) > 0:
            st.info(f"Total de entregas atribuídas: {len(driver)}")
            st.write(driver._Driver__routes_history)  # acessa histórico interno
        else:
            st.warning("Nenhuma entrega registrada.")

    # === Status e Score ===
    st.subheader("🧾 Status do Motorista")
    if st.button("Exibir Status"):
        st.info(str(driver))
        st.write(f"Pontuação atual: {driver._score}")
        st.write(f"Ocorrências registradas: {driver._Driver__occurances}")

#=== Página de Entregas ===
def deliveries_page():
    st.title("📦 Área de Entregas")
    st.markdown("---")
    st.write("Gerencie entregas, atribua motoristas, calcule custos e acompanhe o status.")

    # Inicializa uma entrega na sessão
    if "delivery" not in st.session_state:
        from datetime import datetime
        from project.models.delivery import Delivery   # ajuste conforme seu projeto

        st.session_state.delivery = Delivery(
            id_delivery=1,
            estimated_hours=5,
            distance_km=120,
            id_vehicle="ABC-1234",
            type_vehicle="Caminhão",
            status_vehicle="Disponível",
            capacity_vehicle=2000,
            express=True
        )
    delivery = st.session_state.delivery

    # === Atribuir Motorista ===
    st.subheader("👨‍💼 Atribuir Motorista")
    motorista_nome = st.text_input("Nome do Motorista")
    if st.button("Atribuir Motorista"):
        try:
            delivery.assign_driver(motorista_nome)
            st.success(f"Motorista {motorista_nome} atribuído à entrega.")
        except ValueError as e:
            st.error(str(e))

    # === Iniciar Entrega ===
    st.subheader("🚚 Iniciar Entrega")
    if st.button("Iniciar Entrega"):
        try:
            delivery.start_delivery()
            st.success("Entrega iniciada com sucesso!")
        except PermissionError as e:
            st.error(str(e))

    # === Finalizar Entrega ===
    st.subheader("✅ Finalizar Entrega")
    if st.button("Finalizar Entrega"):
        try:
            delivery.finish_delivery()
            st.success("Entrega finalizada com sucesso!")
        except PermissionError as e:
            st.error(str(e))

    # === Cancelar Entrega ===
    st.subheader("❌ Cancelar Entrega")
    motivo_cancelamento = st.text_input("Motivo do Cancelamento")
    if st.button("Cancelar Entrega"):
        try:
            delivery.cancel_delivery(motivo_cancelamento)
            st.warning(f"Entrega cancelada: {motivo_cancelamento}")
        except PermissionError as e:
            st.error(str(e))

    # === Calcular Custo ===
    st.subheader("💰 Calcular Custo da Entrega")
    if st.button("Calcular Custo"):
        custo = delivery.calculate_cost()
        st.info(f"Custo total da entrega: R${custo:.2f}")

    # === Status da Entrega ===
    st.subheader("📊 Status da Entrega")
    if st.button("Exibir Status"):
        st.info(str(delivery))

    # === Linha do Tempo ===
    st.subheader("🕒 Histórico de Eventos")
    if st.button("Exibir Timeline"):
        timeline = delivery.get_timeline()
        for evento in timeline:
            st.write(f"- {evento['event']} em {evento['date'].strftime('%d/%m/%Y %H:%M:%S')}")



#=== Navegação Principal ===
if menu == "Tela Inicial":
    start_page()
elif menu == "Área Cliente":
    client_page()
elif menu == "Área Produtos":
    product_page()
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