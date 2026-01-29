import streamlit as st
from modules.pages import stock_page
from modules.pages import client_page


def print_management_page():
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
    
    
    st.subheader(" Emissão de Notas Fiscais") 
    with st.form("nota_fiscal_form"):
        cliente = st.selectbox("Selecione o Cliente:", [c['nome'] for c in st.session_state.clientes]) 
        produto = st.selectbox("Selecione o Produto:", [p['nome'] for p in st.session_state.produtos]) 
        quantidade = st.number_input("Quantidade:", min_value=1, value=1) 
        desconto = st.slider("Desconto (%)", 0, 30, 0) 
        emitir = st.form_submit_button("Emitir Nota Fiscal") 
        
    produto_selecionado = next((p for p in st.session_state.produtos if p['nome'] == produto), None)
    
    if produto_selecionado:
        valor_unitario = produto_selecionado.get("preco", 9) 
        valor_total = quantidade * valor_unitario
        valor_final = valor_total * (1 - desconto/100)
    
    st.success("Nota Fiscal Emitida com Sucesso!")
    st.markdown(f""" ### Nota Fiscal - **Cliente:** {cliente}, 
                **Produto:** {produto},
                - **Quantidade:** {quantidade},
                - **Valor Unitário:** R${valor_unitario:.2f},
                - **Valor Total:** R${valor_total:.2f,},
                - **Desconto:** {desconto},
                %- **Valor Final:** R${valor_final:.2f} """)
    st.info("A nota fiscal foi registrada no sistema.")
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
        if st.button("View Clients"):
            menu = "Área Cliente"
            client_page()
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
 
    with col3:
        if st.button("View Employees"):
            menu = "Área Funcionários"
            st.write(st.session_state.funcionarios)
    with col4:
        if st.button("View Deliveries"):
            st.write(st.session_state.entregas)
