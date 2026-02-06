import streamlit as st
import pandas as pd

def print_management_page():
    st.title("Gerenciamento Geral")
    st.write("Área dedicada ao gerenciamento de compras, descontos, funcionários e relatórios estratégicos.")

   
    if "funcionarios" not in st.session_state:
        st.session_state.funcionarios = [
            {"nome": "PEDRO LOBO NUNES", "promovido": False},
            {"nome": "DEMETRIOS COUTINHO", "promovido": True},
            {"nome": "CIRO NUNES", "promovido": False},
            {"nome": "ALUISIO SUPER SALÁRIO", "promovido": False},
        ]

    if "clientes" not in st.session_state:
        st.session_state.clientes = [
            {"nome": "Cliente Teste", "compra_total": 6200, "desconto": 20, "ativo": True, "compra_aprovada": False},
            {"nome": "Cliente Inativo", "compra_total": 1000, "desconto": 5, "ativo": False, "compra_aprovada": False},
        ]

    if "mostrar_relatorio" not in st.session_state:
        st.session_state.mostrar_relatorio = False

    if "msg" not in st.session_state:
        st.session_state.msg = ""

    st.subheader("Minhas Ações")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Aprovar Compras +R$ 5.000"):
            aprovadas = 0
            for c in st.session_state.clientes:
                if c["compra_total"] >= 5000 and not c["compra_aprovada"]:
                    c["compra_aprovada"] = True
                    aprovadas += 1

            st.session_state.msg = (
                f"{aprovadas} compra(s) acima de R$ 5.000 aprovadas."
                if aprovadas else "Nenhuma compra elegível encontrada."
            )
            st.rerun()
            
    with col2:
        if st.button("Aprovar Descontos >= 15%"):
            aprovados = 0
            for c in st.session_state.clientes:
                if c["desconto"] >= 15:
                    c["desconto_aprovado"] = True
                    aprovados += 1

            st.session_state.msg = (
                f"{aprovados} desconto(s) aprovados."
                if aprovados else "Mensagem do Sistema: Nenhum desconto elegível."
            )
            st.rerun()

    with col3:
        if st.button("Mostrar / Ocultar Relatório"):
            st.session_state.mostrar_relatorio = not st.session_state.mostrar_relatorio
            st.rerun()

    if st.session_state.mostrar_relatorio:
        st.subheader("Relatório de Faturamento")

        clientes_ativos = [c for c in st.session_state.clientes if c["ativo"]]
        clientes_inativos = [c for c in st.session_state.clientes if not c["ativo"]]

        total_faturamento = sum(c["compra_total"] for c in clientes_ativos)

        colA, colB, colC = st.columns(3)
        colA.metric("Faturamento Ativo", f"R$ {total_faturamento:,.2f}")
        colB.metric("Clientes Ativos", len(clientes_ativos))
        colC.metric("Clientes Inativos", len(clientes_inativos))

        df = pd.DataFrame({
            "Status": ["Ativos", "Inativos"],
            "Quantidade": [len(clientes_ativos), len(clientes_inativos)]
        }).set_index("Status")

        st.bar_chart(df)

    st.markdown("---")
    
    st.subheader("Sumário Geral do Gerente")

    total_funcionarios = len(st.session_state.funcionarios)
    promovidos = sum(1 for f in st.session_state.funcionarios if f["promovido"])

    total_clientes = len(st.session_state.clientes)
    clientes_ativos = sum(1 for c in st.session_state.clientes if c["ativo"])

    faturamento_total = sum(c["compra_total"] for c in st.session_state.clientes if c["ativo"])
    compras_aprovadas = sum(1 for c in st.session_state.clientes if c.get("compra_aprovada"))
    descontos_aprovados = sum(1 for c in st.session_state.clientes if c.get("desconto_aprovado"))

    col1, col2, col3 = st.columns(3)

    col1.metric("Funcionários", total_funcionarios)
    col1.metric("Promovidos", promovidos)

    col2.metric("Clientes Totais", total_clientes)
    col2.metric("Clientes Ativos", clientes_ativos)

    col3.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
    col3.metric("Compras Aprovadas", compras_aprovadas)
    col3.metric("Descontos Aprovados", descontos_aprovados)

    st.markdown("---")

    st.subheader("Gestão de Employees")

    for i in range(len(st.session_state.funcionarios)):
        f = st.session_state.funcionarios[i]

        col1, col2, col3 = st.columns([3, 2, 2])

        col1.write(f"**{f['nome']}**")
        col2.write("Promovido" if f["promovido"] else "Não foi promovido")

        if col3.button("Promover Employee", key=f"func_{i}"):
            st.session_state.funcionarios[i]["promovido"] = not f["promovido"]
            st.session_state.msg = f"{f['nome']} teve o status alterado."
            st.rerun()

    if st.session_state.msg:
        st.success(st.session_state.msg)
        
print_management_page()
