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
    st.write("Gerencie suas vendas, clientes atendidos, comissões e metas mensais.")


    if "seller" not in st.session_state: 
        
        st.session_state.seller = Seller(
            region="RN",
            name="José da Almeida Fonseca",
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
            commision_percentual=10,
            hours_worked=9,
            
        )
        
    beneficios_categoria = {
    "Diamante": [
        "Possui  20% de desconto exclusivo",
        "Atendimento prioritário",
        "Crédito Estendido",
        "Negociação personalizada com a distribuidora"
       
    ],
    "Ouro": [
        "10% de desconto em compras",
        "Atendimento prioritário",
        "Crédito Facilitado pela distribuidora"
    ],
    "Prata": [
        "Programa de fidelidade padrão",
        "Frete grátis"
    ],
    "Bronze": [
        "Condições comerciais básicas"
    ]
}
    
    seller = st.session_state.seller

    st.subheader("Registrar Cliente Atendido")
    cliente_nome = st.text_input("Nome do Cliente Atendido")
    if st.button("Registrar Atendimento"):
        seller.attend_costumer(cliente_nome)
        st.success(f"Mensagem do Sistema: Cliente {cliente_nome} registrado como atendido.")

  
    st.subheader("Registrar Venda")
    cliente_venda = st.text_input("Cliente da Venda")
    produto_venda = st.text_input("Produto Vendido")
    qtd_venda = st.number_input("Quantidade", min_value=1, step=1)
    if st.button("Registrar Venda"):
        seller.make_sale(cliente_venda, produto_venda, qtd_venda)
        seller.add_pallets_sold(qtd_venda)
        st.success(f"Mensagem do Sistema: Venda registrada: {qtd_venda}x {produto_venda} para {cliente_venda}")


    st.subheader("Negociar Preço")
    desconto = st.slider("Selecione o desconto (%)", 0.0, 0.15, 0.05)
    if st.button("Negociar"):
        st.info(seller.negotiate_price(desconto))


    st.subheader("Responder Reclamação")
    cliente_reclamacao = st.text_input("Cliente com Reclamação")
    if st.button("Responder Reclamação"):
        st.success(seller.respond_to_complaint(cliente_reclamacao))

  
    st.subheader("Verificar Crédito do Cliente")
    cliente_credito = st.text_input("Nome do Cliente")
    if st.button("Verificar Crédito"):
        class FakeClient:
            def __init__(self, name, credit_score):
                self.name = name
                self.credit_score = credit_score
        fake_client = FakeClient(cliente_credito, 650)
        st.info(seller.see_costumer_credit(fake_client))

    st.subheader("Acompanhamento e Benefícios")
    cliente_acomp = st.text_input("Acompanhar Cliente")
    if st.button("Fazer Acompanhamento"):
        st.success(seller.follow_costumer(cliente_acomp))
        
    if st.button("Pôr Benefício Para o Cliente"):
        pontos_cliente  = seller.apply_costumer_benefi(cliente_acomp)
        categoria = classify_client(pontos_cliente)
        
        beneficios = beneficios_categoria.get(categoria, [])
        
        st.success(f"Benefício aplicado ao cliente {cliente_acomp}")
        st.info(f"Categoria Atual: {categoria}")

        st.markdown("Benefícios aplicados ao cliente:")
        for b in beneficios:
            st.info(f"-{b}")

    st.subheader("Solicitar Avaliação")
    nota = st.number_input("Nota (1 a 5)", min_value=1, max_value=5, step=1)
    if st.button("Registrar Avaliação"):
        try:
            seller.request_evaluation(nota)
            st.success("Avaliação registrada com sucesso.")
        except ValueError as e:
            st.error(str(e))
            
    st.subheader("Sumário de Vendas")
    
    resumo = {
            "clientes_atendidos": 10,
            "vendas_realizadas": 78,
            "paletes_vendidos": 456,
            "comissao": 100
        }
    
    if st.button("Exibir Sumário"):
        resumo = seller.sumary_sales()
    
    df_resumo = pd.DataFrame({
        "Métrica": ["Clientes Atendidos", "Vendas Realizadas", "Paletes Vendidos", "Comissão (R$)"],
        "Valor": [resumo["clientes_atendidos"], resumo["vendas_realizadas"], resumo["paletes_vendidos"], resumo["comissao"]]
    })
    
  
    st.dataframe(df_resumo)
