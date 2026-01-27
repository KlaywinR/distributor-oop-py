from abc import ABC, abstractmethod

class AbstractSeller(ABC):
    """
    Cria um vendedor base para atender os clientes, o mesmo faz venda e calcula comissão percentual.
    """
    @abstractmethod
    def make_sale(self, costumer, product, quantity):
        pass
    
    @abstractmethod
    def calculate_comissions(self):
        pass
