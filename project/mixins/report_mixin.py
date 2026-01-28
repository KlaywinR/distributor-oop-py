  
class ReportMixin:
    """
    Responsável pela geração de relatórios do sistema.
    - SRP: fornecendo métricas de faturamento e clientes ativos.
    """
    def total_revenue(self):
        """
        Calcula o faturamento das compras concluidas
        """
        return sum(p.total_value for p in self._purchases if p.status == "COMPLETED")
    
    def active_clients(self):
        """"
        Retorna a lista de clientes ativos no sitema.
        """
        return [c for c in self._clients if c.client_status() == "Cliente Ativo"]