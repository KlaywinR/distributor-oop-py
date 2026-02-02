import streamlit as st
from datetime import date 
from project.models.seller import Seller 
import pandas as pd 


def classify_client(loyalty_points):
    try:
        loyalty_points = int(loyalty_points)
    except ValueError:
        loyalty_points = 0
    
    if loyalty_points >= 100:
        return "Diamante"
    if loyalty_points >= 70:
        return "Ouro"
    if loyalty_points >= 40:
        return "Prata"
    else:
        return "Bronze"
  
def print_seller_page():
    st.title(" Área do Vendedor")
    st.markdown("---")
    st.write("Gerencie suas vendas, clientes atendidos, comissões e metas mensais.")


    if "seller" not in st.session_state: 
        
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

    st.subheader("Acompanhamento e Benefícios")
    cliente_acomp = st.text_input("Cliente para acompanhamento")
    if st.button("Fazer Acompanhamento"):
        st.success(seller.follow_costumer(cliente_acomp))
        
    if st.button("Aplicar Benefício"):
        pontos_cliente  = seller.apply_costumer_benefi(cliente_acomp)
        categoria = classify_client(pontos_cliente)
        st.success(f"Beneficio aplicado ao cliente {cliente_acomp} | Categoria Atual: **{categoria}**")

    st.subheader("Solicitar Avaliação")
    nota = st.number_input("Nota (1 a 5)", min_value=1, max_value=5, step=1)
    if st.button("Registrar Avaliação"):
        try:
            seller.request_evaluation(nota)
            st.success("Avaliação registrada com sucesso.")
        except ValueError as e:
            st.error(str(e))

    st.subheader("Sumário de Vendas")
    if st.button("Exibir Sumário"):
        resumo = seller.sumary_sales()
        
    
    df_resumo = pd.DataFrame({
        "Métrica": ["Clientes Atendidos", "Vendas Realizadas", "Paletes Vendidos", "Comissão (R$)"],
        "Valor": [resumo["clientes_atendidos"], resumo["vendas_realizadas"], resumo["paletes_vendidos"], resumo["comissao"]]
    })
    
  
    st.markdown("### Tabela Resumo")
    st.table(df_resumo.style.format({"Valor": "{:,.0f}"}))
    
   
    st.markdown("### Gráfico de Desempenho")
    st.bar_chart(df_resumo.set_index("Métrica"))
    
   
    st.markdown("### Indicadores em Destaque")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Clientes Atendidos", resumo["clientes_atendidos"])
    col2.metric("Vendas Realizadas", resumo["vendas_realizadas"])
    col3.metric("Paletes Vendidos", resumo["paletes_vendidos"])
    col4.metric("Comissão (R$)", f"R$ {resumo['comissao']:.2f}")

st.markdown("---")

