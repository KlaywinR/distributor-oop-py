import streamlit as st
from modules.pages import stock_page
from modules.pages import client_page
import random


def print_management_page():
    st.title("Gerenciamento Geral")
    st.markdown("---")
    st.write("Área dedicada ao gerenciamento de compras, descontos, funcionários e relatórios estratégicos.")
 

    st.subheader("Minhas Ações")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Aprovar Compras +R$ 5.000"):
            aprovadas = 0
            for c in st.session_state.clientes:
                if c.get("compra_total", 0) >= 5000 and not c.get("compra_aprovada", False):
                    c["compra_aprovada"] = True
                    aprovadas += 1
                    st.success(
                        f"Compra de R${c['compra_total']:.2f} do cliente {c['nome']} foi APROVADA."
                    )

            if aprovadas == 0:
                st.warning("Mensagem do Sistema: Nenhuma compra acima de R$ 5.000 encontrada.")

    with col2:
        if st.button("Aprovar Descontos >= 15%"):
            descontos = [c for c in st.session_state.clientes if c.get("desconto", 0) >= 15]
            if descontos:
                for c in descontos:
                    st.success(
                        f"Desconto de {c['desconto']}% para o cliente {c['nome']} foi APROVADO."
                    )
            else:
                st.warning("Mensagem do Sistema: Nenhum desconto elegível encontrado.")

    with col3:
        if st.button("Exibir Relatório de Faturamento"):
            total_faturamento = sum(c.get("compra_total", 0) for c in st.session_state.clientes)
            clientes_ativos = [c for c in st.session_state.clientes if c.get("ativo", True)]
            inativos = len(st.session_state.clientes) - len(clientes_ativos)

            st.info(f"Faturamento total: R${total_faturamento:.2f}")
            st.info(f"Clientes ativos: {len(clientes_ativos)}")
            st.info(f"Clientes inativos: {inativos}")

            dados_grafico = {
                "Ativos": len(clientes_ativos),
                "Inativos": inativos,
            }
            st.bar_chart(dados_grafico)

    st.markdown("---")

    # ==========================
    # GESTÃO DE EMPLOYEES
    # ==========================


st.subheader("Gestão de Employeees")

# cria os dados uma única vez
if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = [
        {"nome": "João", "promovido": False},
    ]


if "messages" not in st.session_state:
    st.session_state.messages = ""
    
# mostra na tela
for i in range(len(st.session_state.funcionarios)):
    f = st.session_state.funcionarios[i]

    st.write(f"Nome: {f['nome']}")

    texto = "Promover" if not f['promovido'] else "Rebaixar"

    if st.button(texto, key=i):
        st.session_state.funcionarios[i]['promovido'] = not f['promovido']
        
        if st.session_state.funcionarios[i]['promovido']:
            st.session_state.message = f"{f['nome']} foi promovido na empresa"
        else: 
            st.session_state.msg = f"{f['nome']} foi REBAIXADO."
    
        st.rerun()
    
    st.write("---")
    
if st.session_state.msg:
    st.success(st.session_state.msg)
    


    st.subheader("Emissão de Notas Fiscais")

    if "notas_fiscais" not in st.session_state:
        st.session_state.notas_fiscais = []

    if "nota_emitida" not in st.session_state:
        st.session_state.nota_emitida = None

    with st.form("nota_fiscal"):
        cliente = st.selectbox("Cliente:", [c["nome"] for c in st.session_state.clientes])
        produto = st.selectbox("Produto:", [p["nome"] for p in st.session_state.produtos])
        quantidade = st.number_input("Quantidade:", min_value=1)
        desconto = st.slider("Desconto (%)", 0, 30)
        emitir = st.form_submit_button("Emitir Nota")

    if emitir:
        prod = next(
            (p for p in st.session_state.produtos if p["nome"] == produto),
            None,
        )

        if not prod:
            st.error("Produto não encontrado")
            st.stop()

        valor_total = quantidade * prod["preco"]
        valor_final = valor_total * (1 - desconto / 100)

        st.session_state.nota_emitida = {
            "cliente": cliente,
            "produto": produto,
            "quantidade": quantidade,
            "valor_final": valor_final,
        }

        st.session_state.notas_fiscais.append(st.session_state.nota_emitida)

    if st.session_state.nota_emitida:
        st.success("Nota Fiscal Emitida com Sucesso!")
        st.json(st.session_state.nota_emitida)

   
    st.subheader("Dashboard do Sistema")

    if "dashboard" not in st.session_state:
        st.session_state.dashboard = None

    if st.button("Exibir Painel"):
        st.session_state.dashboard = {
            "Clientes": random.randint(5, 9),
            "Produtos": random.randint(0, 340),
            "Funcionários": random.randint(9, 45),
            "Entregas": random.randint(9, 23),
            "Estoque": random.randint(9, 67),
        }

    if st.session_state.dashboard:
        dados = st.session_state.dashboard

        col1, col2, col3 = st.columns(3)
        col1.metric("Clientes", dados["Clientes"])
        col2.metric("Produtos", dados["Produtos"])
        col3.metric("Entregas", dados["Entregas"])

        st.markdown("### Visão Geral")
        st.bar_chart(dados)

    st.markdown("---")
