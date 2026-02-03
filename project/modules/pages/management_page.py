import streamlit as st
import pandas as pd

def print_management_page():
    st.title("Gerenciamento Geral")
    st.write("Área dedicada ao gerenciamento de compras, descontos, funcionários e relatórios estratégicos.")

  
    st.session_state.setdefault(
        "funcionarios",
        [
            {"nome": "PEDRO LOBO NUNES", "promovido": False},
            {"nome": "DEMETRIOS COUTINHO", "promovido": True},
            {"nome": "CIRO NUNES", "promovido": False},
            {"nome": "ALUISIO SUPER SALÁRIO", "promovido": False},
        ],
    )
    st.session_state.setdefault("msg", "")
    st.session_state.setdefault(
        "clientes",
        [{"nome": "Cliente Teste", "compra_total": 6200, "desconto": 20, "ativo": True},
         {"nome": "Cliente Inativo", "compra_total": 1000, "desconto": 20, "inativo": False}],
        
    )
    st.session_state.setdefault("mostrar_relatorio", False)

   
    st.subheader("Minhas Ações")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Aprovar Compras +R$ 5.000"):
            aprovadas = 0
            for c in st.session_state.clientes:
                if c.get("compra_total", 0) >= 5000 and not c.get("compra_aprovada", False):
                    c["compra_aprovada"] = True
                    aprovadas += 1
            st.session_state.msg = (
                f"{aprovadas} compra(s) acima de R$ 5.000 foram aprovadas."
                if aprovadas else "Nenhuma compra acima de R$ 5.000 encontrada."
            )

    with col2:
        if st.button("Aprovar Descontos >= 15%"):
            descontos = [c for c in st.session_state.clientes if c.get("desconto", 0) >= 15]
            st.session_state.msg = (
                f"{len(descontos)} desconto(s) aprovados."
                if descontos else "Nenhum desconto elegível encontrado."
            )

    with col3:
        if st.button("Exibir Relatório de Faturamento"):
            st.session_state.mostrar_relatorio = True


    if st.session_state.mostrar_relatorio:
        total_faturamento = sum(c.get("compra_total", 0) for c in st.session_state.clientes)
        clientes_ativos = [c for c in st.session_state.clientes if c.get("ativo", True)]
        inativos = len(st.session_state.clientes) - len(clientes_ativos)

        st.markdown("Resumo Geral")
        colA, colB, colC = st.columns(3)
        colA.metric("Faturamento Total", f"R${total_faturamento:.2f}")
        colB.metric("Clientes Ativos", len(clientes_ativos))
        colC.metric("Clientes Inativos", inativos)

        df = pd.DataFrame({
            "Status": ["Ativos", "Inativos"],
            "Quantidade": [len(clientes_ativos), inativos]
        }).set_index("Status")

        st.bar_chart(df)

    st.markdown("---")

  
    st.subheader("Gestão de Employees")
    st.markdown("---")
    for i, f in enumerate(st.session_state.funcionarios):
        col_nome, col_status, col_btn = st.columns([2, 2, 1])
        with col_nome:
            st.write(f"**{f['nome']}**")
        with col_status:
            status = "Foi Promovido" if f["promovido"] else "Não foi condecorado"
            st.write(status)
        with col_btn:
            texto = "Promover Employee" if not f["promovido"] else "Não promover employee"
            if st.button(texto, key=f"func_{i}"):
                f["promovido"] = not f["promovido"]
                st.session_state.msg = (
                    f"{f['nome']} foi promovido na empresa"
                    if f["promovido"] else f"{f['nome']} foi REBAIXADO."
                )

    st.markdown("---")
    if st.session_state.msg:
        st.success(st.session_state.msg)

print_management_page()
