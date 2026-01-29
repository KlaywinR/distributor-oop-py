import streamlit as st
from pages import client_page
from pages import stock_page
from pages import orders_page


def start_page():
    st.title("Sistema DistriSys")
    st.markdown("---")

    st.subheader("Olá, seja bem-vindo!")
    st.write("Este é o painel inicial do sistema. Você pode navegar rapidamente para qualquer área e visualizar um resumo de operações.")

    st.subheader("Fast Acess")
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

    st.subheader("Summary Geral")
    dados_dashboard = {
        "Clientes": len(st.session_state.clientes),
        "Produtos": len(st.session_state.produtos),
        "Funcionários": len(st.session_state.funcionarios),
        "Entregas": len(st.session_state.entregas),
        "Estoque": len(st.session_state.estoque)
    }
    st.bar_chart(dados_dashboard)

    st.markdown("---")

    st.subheader("Interaja com o DistriSys")
    username = st.text_input("Digite seu nome:")
    humor = st.selectbox(f"Olá! {username} Como você está se sentindo hoje?", [" Ótimo", "Muito Bem", "Estou Neutro", "Muito Cansado"])
    if st.button("Enviar Respostas"):
        st.success(f"Olá, {username} que bom ter você aqui! Vejo que está se sentindo {humor}. Vamos tornar sua experiência ainda mais produtiva!")
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

