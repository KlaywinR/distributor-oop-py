import streamlit as st

def print_orders_page():
    st.subheader("Gestão de Pedidos")
    st.markdown("---")
    st.write("Esta Área é dedicada ao registro, acompanhamento e análise de pedidos dos clientes.")

    st.subheader("Criar Novo Pedido")
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