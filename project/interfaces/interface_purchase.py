
from abc import ABC, abstractmethod
            
class InterfacePurchase(ABC):
    
    @abstractmethod
    def calculate_total(self):
        """
        Calcula o total da compra
        """
        pass
    
    @abstractmethod
    def finalize_purchase(self):
        """
        Finaliza a compra
        """
        pass
    
    @abstractmethod
    def cancel_purchase(self):
        """
        Cancela a compra.
        """
        pass
    
    @abstractmethod
    def reserve_pallets(self):
        """
        Reserva pallets por encomenda.
        """
        pass
    