
from abc import ABC,abstractmethod

class DistributorInterface(ABC):
    """
    Princípio da Inversão de Dependência (DIP),
    definindo contratos para registro de entidades,
    processamento de compras e despacho de entregas.
    """

    @abstractmethod
    def register_client(self, client):
        """
        Registra um cliente
        """
        pass
    
    @abstractmethod
    def register_employee(self, employee):
        """
        Registra um empregado
        """
        pass
    
    @abstractmethod
    def register_stock(self, stock):
        """
        Registra um estoque
        """
        pass
    
    @abstractmethod
    def process_purchase(self, purchase):
        """
        Registra o processamento de uma compra.
        """
        pass
    
    @abstractmethod
    def dispatch_delivery(self, delivery):
        """
        Registra o despacho da entrega.
        """
        pass
    