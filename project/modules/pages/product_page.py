import streamlit as st

def product_page():
    st.title("Gestão de Produtos")
    st.markdown("---")
    if st.button("Adicionar Preço Promocional"):
            for p in st.session_state.estoque:
                p.preco_promocional = p.preco_unitario * 0.9  #10% de desconto
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
