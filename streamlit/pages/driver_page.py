import streamlit as st
from datetime import date
from project.models.driver import Driver   

def driver_page():
    st.title("  Área do Motorista")
    st.markdown("---")
    st.write("Gerencie entregas, ocorrências, disponibilidade e status do motorista.")

    if "driver" not in st.session_state:
        st.session_state.driver = Driver(
            id_driver=1,
            name="José Ferreira",
            cpf="987.654.321-00",
            cnh_category="D",
            cnh_expiration=date(2027, 5, 20),
            max_capacity_pallets=100,
            region="Nordeste"
        )
    driver = st.session_state.driver


    st.subheader(" Validade da CNH")
    if st.button("Verificar CNH"):
        if driver.cnh_is_valid():
            st.success("CNH válida ")
        else:
            st.error("CNH vencida")

    st.subheader(" Disponibilidade para Operar")
    if st.button("Verificar Disponibilidade"):
        if driver.can_operate():
            st.success("Motorista pode operar ")
        else:
            st.error("Motorista não pode operar")

    st.subheader(" Atribuir Entrega")
    entrega_nome = st.text_input("Nome da Entrega")
    if st.button("Atribuir Entrega"):
        try:
            driver.assign_delivery(entrega_nome)
            st.success(f"Entrega '{entrega_nome}' atribuída ao motorista.")
        except PermissionError as e:
            st.error(str(e))

    st.subheader(" Rejeitar Entrega")
    if st.button("Rejeitar Entrega"):
        driver.reject_delivery()
        st.warning("Entrega rejeitada e ocorrência registrada.")

    st.subheader(" Registrar Ocorrência")
    ocorrencia = st.text_input("Descrição da Ocorrência")
    if st.button("Registrar Ocorrência"):
        driver.register_occurance(ocorrencia)
        st.success(f"Ocorrência registrada: {ocorrencia}")
        
    st.subheader(" Histórico de Entregas")
    if st.button("Exibir Histórico"):
        if len(driver) > 0:
            st.info(f"Total de entregas atribuídas: {len(driver)}")
            st.write(driver._Driver__routes_history) 
            st.warning("Nenhuma entrega registrada.")

    st.subheader("  Status do Motorista")
    if st.button("Exibir Status"):
        st.info(str(driver))
        st.write(f"Pontuação atual: {driver._score}")
        st.write(f"Ocorrências registradas: {driver._Driver__occurances}")
