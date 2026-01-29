import streamlit as st
from datetime import datetime
from project.models.delivery import Delivery   


def print_deliveries_page():
    st.title(" Área de Entregas")
    st.markdown("---")
    st.write("Gerencie entregas, atribua motoristas, calcule custos e acompanhe o status.")

    if "delivery" not in st.session_state:
      

        st.session_state.delivery = Delivery(
            id_delivery=1,
            estimated_hours=5,
            distance_km=120,
            id_vehicle="ABC-1234",
            type_vehicle="Caminhão",
            status_vehicle="Disponível",
            capacity_vehicle=2000,
            express=True
        )
    delivery = st.session_state.delivery

    st.subheader(" Atribuir Motorista")
    motorista_nome = st.text_input("Nome do Motorista")
    if st.button("Atribuir Motorista"):
        try:
            delivery.assign_driver(motorista_nome)
            st.success(f"Motorista {motorista_nome} atribuído à entrega.")
        except ValueError as e:
            st.error(str(e))

    st.subheader(" Iniciar Entrega")
    if st.button("Iniciar Entrega"):
        try:
            delivery.start_delivery()
            st.success("Entrega iniciada com sucesso!")
        except PermissionError as e:
            st.error(str(e))

    st.subheader(" Finalizar Entrega")
    if st.button("Finalizar Entrega"):
        try:
            delivery.finish_delivery()
            st.success("Entrega finalizada com sucesso!")
        except PermissionError as e:
            st.error(str(e))

    st.subheader(" Cancelar Entrega")
    motivo_cancelamento = st.text_input("Motivo do Cancelamento")
    if st.button("Cancelar Entrega"):
        try:
            delivery.cancel_delivery(motivo_cancelamento)
            st.warning(f"Entrega cancelada: {motivo_cancelamento}")
        except PermissionError as e:
            st.error(str(e))

    st.subheader("Calcular Custo da Entrega")
    if st.button("Calcular Custo"):
        custo = delivery.calculate_cost()
        st.info(f"Custo total da entrega: R${custo:.2f}")

    st.subheader("Status da Entrega")
    if st.button("Exibir Status"):
        st.info(str(delivery))

    st.subheader("Histórico de Eventos")
    if st.button("Exibir Timeline"):
        timeline = delivery.get_timeline()
        for evento in timeline:
            st.write(f"- {evento['event']} em {evento['date'].strftime('%d/%m/%Y %H:%M:%S')}")