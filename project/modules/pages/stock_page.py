
import streamlit as st
from project.models.product.product import Product


def print_stock_page():
    st.title("Gestão do Estoque")
    st.markdown("---")

    stock = st.session_state.stock_obj
    

    st.subheader("Cadastro de Pallets")
    with st.form("form_add_pallet"):
        nome = st.text_input("Nome do Produto/Pallet") 
        quantidade = st.number_input("Quantidade", min_value=1, step=1) 
        preco_unitario = st.number_input("Preço Unitário - R$", min_value=0.0, step=0.01) 
        marca = st.text_input("Marca do Produto")
        categoria = st.text_input("Categoria do Produto")
        fornecedor = st.text_input("Nome do Fornecedor")
        validade = st.date_input("Data de Validade")
        is_active = st.checkbox("O Produto está ativo?", value=True) 
        submitted = st.form_submit_button("Colocar no Estoque")

        if submitted:
            if is_active:
                try:
                
                    produto_obj = Product(
                        name=nome,
                        category=categoria,
                        unit_measure="UN",
                        brand=marca,
                        wheight_per_unit=1.0,
                        pallets_quantity=int(quantidade),
                        barcode=f"BAR_{nome}_{fornecedor}",
                        total_units=int(quantidade),
                        cost_price=preco_unitario,
                        quantity=int(quantidade),
                        supplier=fornecedor,
                        min_stock=1,
                        origin="Distribuidor",
                        units_per_pallet=1,
                        min_pallets=1,
                        unit_price=preco_unitario,
                        expiration_date=validade
                    )
                    
                    stock.add_pallet(produto_obj, int(quantidade))
                    
                    #compatibilidade com o estoque
                    novo_produto = {
                        "nome": nome,
                        "quantidade": quantidade,
                        "preco": preco_unitario,
                        "marca": marca,
                        "categoria": categoria,
                        "fornecedor": fornecedor,
                        "validade": validade,
                        "status": "Ativo" if is_active else "Inativo"
                    }
                    st.session_state.estoque.append(novo_produto)
                    st.session_state.produtos.append(novo_produto)  
                    st.success(f"{quantidade} paletes de {nome} adicionados ao estoque e vinculados à gestão de produtos.")
                except Exception as e:
                    st.error(f"Mensagem do Sistema: Erro ao adicionar produto: {str(e)}")
            else:
                st.error(f"Mensagem do Sistema: O pallet '{nome}' está vencido e não pode ser adicionado.")

    st.markdown("---")

    st.subheader("Remoção de Pallets")
    if st.session_state.estoque:
        produto_remover = st.selectbox("Selecione o produto para remover:", [p["nome"] for p in st.session_state.estoque])
        qtd_remover = st.number_input("Quantidade para remoção", min_value=1, step=1)
        confirmar = st.checkbox("Confirmar remoção do produto selecionado")
        if st.button("Desejo Remover Pallet"):
            produto_encontrado_estoque = None
            for p in st.session_state.estoque:
                if p["nome"] == produto_remover:
                    produto_encontrado_estoque = p
                    break
            
            if produto_encontrado_estoque:
                if produto_encontrado_estoque["quantidade"] >= qtd_remover and confirmar:
                    try:
                        #produto correspondente no estoque
                        produto_encontrado = None
                        for item in stock.list_pallets():
                            if item.product.name == produto_remover:
                                produto_encontrado = item.product
                                break
                        
                        if produto_encontrado:
                            stock.del_pallet(produto_encontrado, qtd_remover)
                            produto_encontrado_estoque["quantidade"] -= qtd_remover
                            
                            if produto_encontrado_estoque["quantidade"] == 0:
                                st.session_state.estoque.remove(produto_encontrado_estoque)
                             
                            for prod in st.session_state.produtos:
                                if prod["nome"] == produto_remover:
                                    prod["quantidade"] = produto_encontrado_estoque["quantidade"]
                                    if prod["quantidade"] == 0:
                                        st.session_state.produtos.remove(prod)
                            
                            st.success(f"{qtd_remover} paletes de {produto_remover} removidos do estoque.")
                        else:
                            st.error(f"Mensagem do sistema: Produto '{produto_remover}' não encontrado no estoque de objetos.")
                    except ValueError as e:
                        st.error(f"Mensagem do Sistema: Erro ao remover: {str(e)}")
                else:
                    st.error("Mensagem do Sistema: Quantidade insuficiente ou remoção não confirmada.")
    else:
        st.warning("Mensagem do Sistema: O Estoque se encontra vazio, não há pallets para remover.")

    st.markdown("---")

  
    st.subheader("Listagem de Pallets e Valor Total")
    if st.button("Listar Todos os Pallets"):
        estoque_atualizado = []
        
        for item in stock.list_pallets():
            estoque_atualizado.append({
                "nome": item.product._name,
                "quantidade": item.pallets,
                "preco": item.product.current_price(),
                "marca": item.product._brand,
                "categoria": item.product._category,
                "fornecedor": item.product._supplier,
                "validade": item.product._expiration_date,
                "status": "Ativo" if item.product.is_active() else "Inativo"
            })
        
        if estoque_atualizado:
            valor_total = sum(p["preco"] * p["quantidade"] for p in estoque_atualizado)
            for p in estoque_atualizado:
                st.info(
                    f"**Produto:** {p['nome']} | "
                    f"**Quantidade:** {p['quantidade']} | "
                    f"**Preço Unitário:** R${p['preco']:.2f} | "
                    f"**Marca:** {p.get('marca', 'Não informado')} | "
                    f"**Categoria:** {p.get('categoria', 'Não informado')} | "
                    f"**Fornecedor:** {p.get('fornecedor', 'Não informado')} | "
                    f"**Validade:** {p.get('validade', 'Não informado')} | "
                    f"**Status:** {p.get('status', 'Ativo')}"
                )
            st.success(f"    Valor total do estoque: R${valor_total:.2f}")
            st.info(f"   Total de pallets: {sum(p['quantidade'] for p in estoque_atualizado)}")
        else:
            st.warning("Estoque vazio.")

    st.markdown("---")

    st.subheader("Informações Gerais do Estoque")
    if st.button("Desejo Mostrar Informações"):
        if st.session_state.estoque:
            valor_total = sum(p["preco"] * p["quantidade"] for p in st.session_state.estoque)
            quantidade_total = sum(p["quantidade"] for p in st.session_state.estoque)
            capacidade_total = st.session_state.capacidade_total

            st.write(f"**Responsável pelo Estoque:** {st.session_state.responsavel_estoque}")
            st.write(f"**Capacidade Máxima:** {capacidade_total} pallets")
            st.write(f"**Ocupação Atual:** {quantidade_total}/{capacidade_total} pallets")

            ocupacao = quantidade_total / capacidade_total
            st.progress(min(ocupacao, 1.0))

            dados = {
                "Métrica": ["Valor Total (R$)", "Quantidade Total"],
                "Valor": [valor_total, quantidade_total]
            }
            st.bar_chart(dados, x="Métrica", y="Valor")
        else:
            st.warning("Estoque vazio.")