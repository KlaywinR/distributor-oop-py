import streamlit as st

if "produtos" not in st.session_state:
    st.session_state.produtos = []

st.set_page_config(
    page_title="SISTEMA DE GESTÃO COMERCIAL E LOGÍSTICA DE DISTRIBUIDORA", layout="wide"    
)

st.title("SISTEMA DE GESTÃO COMERCIAL E LOGÍSTICA DE DISTRIBUIDORA")

menu = st.sidebar.radio(
    "Menu",
    ["Início", "Área do Cliente", "Área de Produtos", "Estoque", "Pedidos", "Gerência Geral"]
)

st.write(f"Tela atual: {menu}")

def start_page():
    st.subheader("Início")
    st.write("Tela inicial do sistema")
    
def product_page():
    st.subheader("Gestão de Produtos")
    
    st.write("Produtos cadastrados:")
        
    for p in st.session_state.produtos:
        st.write(
            f"- {p ['nome']} | R${p['preco']} | Quant: {p['quantidade']}"
        )
    
    if "mostrar_form" not in st.session_state:
        st.session_state.mostrar_form = False
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("➕ Cadastrar Produtos"):
            st.session_state.mostrar_form = True
            
    with col2:
        if st.button("🏷️ Adicionar Promoção"):
            st.session_state.add_promotion = True
            
    with col3:
        if st.button("🔄 Remover Promoção"):
            st.session_state.remove_promotion = True          
    
    with col4:
        if st.button("📆 Ver Data de Validade"):
            st.session_state.see_valid_date = True
            
    with col5:
        if st.button("📦 Calcular Unidades"):
            st.session_state.calculate_units_pallets = True
    
    if st.session_state.mostrar_form:
        with st.form("form_produto"):
            
            name = st.text_input("Nome do produto:")
            price = st.number_input("Preço:")
            quantity = st.number_input("Quantidade:")

            submitted = st.form_submit_button("Cadastrar")
            
            if submitted:
                
                product = {
                    'nome' : name,
                    'preco' : price,
                    'quantidade' : quantity,
                }
                st.session_state.produtos.append(product)
                st.success("Produto cadastrado com sucesso!")
            
        st.divider()
        
                
            
        

def client_page():
    st.subheader("Clientes")
    st.write("Seja bem-vindo(a), nós da distribuidora FULANO DE TAL estamos aqui para fazer o melhor por você")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🛒Comprar"):
            pass
    
    with col2:
        if st.button("📊Desconto por volume"):
            pass
        
    with col3:
        if st.button("⭐Adicionar Pontos Fidelidade"):
            pass
        
    with col4:
        if st.button("🎁Reivindicar Pontos"):
            pass
        
    with col5:
        if st.button("🔍Checar Promoções"):
            pass
        
    with col6:
        if st.button("💬Avaliar serviço"):
            pass
    
def orders_page():
    st.subheader("Pedidos")
    st.write("Tela de pedidos")
    
def stock_page():
    st.subheader("Estoque")
    st.write("Acompanhamento do estoque")
    
def general_management():
    st.subheader("Gerência")
    st.write("Gerenciamento geral da distribuidora")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("🛒 Aprovação de compras")
        valor = st.number_input(
            "Valor da compra",
            min_value=0.0,
            step=100.0,
            key="valor_compra"
        )

        if st.button("Aprovar compra"):
            if gerente.aprovar_compra(valor):
                st.success("✅ Compra de alto valor APROVADA!")
            else:
                st.error("❌ Compra não necessita aprovação do gerente.")

    with col2:
        st.write("📉 Aprovação de desconto")
        desconto = st.number_input(
            "Desconto (%)",
            min_value=0,
            max_value=100,
            key="desconto"
        )

        if st.button("Aprovar desconto"):
            if gerente.aprovar_desconto(desconto):
                st.success("✅ Desconto APROVADO!")
            else:
                st.warning("⚠️ Desconto abaixo do permitido.")
        
    with col3:
         if st.button("📊 Relatórios"):
            faturamento = gerente.relatorio_faturamento()
            clientes = gerente.clientes_ativos()

            st.info(f"💰 Faturamento total: R$ {faturamento:.2f}")
            st.write(f"👥 Clientes ativos: {clientes}")
        
    with col4:
       if st.button("👔 Gerir funcionários"):
            resultados = gerente.gerir_funcionarios()

            for nome, promovido in resultados.items():
                if promovido:
                    st.success(f"✅ {nome} — AUTORIZADO")
                else:
                    st.warning(f"⚠️ {nome} — não autorizado")

if menu == "Início":
    start_page()

elif menu == "Área do Cliente":
    client_page()
    
elif menu == "Área de Produtos":
    product_page()
    
elif menu == "Estoque":
    stock_page()
    
elif menu == "Pedidos":
    orders_page()
    
elif menu == "Gerência Geral":
    general_management()