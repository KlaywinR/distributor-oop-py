class ReportMixin:
    """
    Responsável pela geração de relatórios de vendas.
    """
    def generate_report(self, seller):
        """"
        Gera um relatório de vendas do vendedor informado.
        """
        return   f"""
        Relatório de Vendas:
        - Clientes atendidos: {len(seller._Seller__costumers_served)}
        - Vendas realizadas: {len(seller._Seller__sales_made)}
        - Paletes vendidos: {seller._Seller__pallets_sold}
        - Comissão: {seller.calculate_comissions()}
        """
