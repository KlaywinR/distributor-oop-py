class ReportAggregator:
    """Agregador de relatórios do sistema.
    
    - SRP: apenas agrega e organiza dados.
    - DIP: depende de objetos que expõem interfaces.
    - OCP: novos relatórios podem ser adicionados sem alterar
      entidades existentes.
    """
    def __init__(self, clients, sellers, products, deliveries):
        self.clients = clients
        self.sellers = sellers
        self.products = products
        self.deliveries = deliveries

    def dashboard(self):
        return {
            "Clientes": [c.summary_client() for c in self.clients],
            "Vendedores": [s.sumary_sales() for s in self.sellers],
            "Produtos": [p.__str__() for p in self.products],
            "Entregas": [d.summary_delivery() for d in self.deliveries]
        }
