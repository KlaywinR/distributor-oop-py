from abc import ABC, abstractmethod

class LoyaltySystem(ABC):
    """
    Classe abstrata base para um sistema de fidelidade.
    """
    @abstractmethod
    def claim_points(self):
        """
        Resgate de pontos
        """
        pass
    
    @abstractmethod
    def add_loyalty_points(self, buy_value):
        """
        Adiciona pontos acumulativos acerca do valor da compra.
        """
        pass
    