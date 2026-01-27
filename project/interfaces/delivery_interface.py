
from abc import ABC, abstractmethod

class DeliveryInterface(ABC):
    """
    Interface base para controle do ciclo de uma entrega.
    """
    
    @abstractmethod
    def start_delivery(self):
        """
        Inicia o processo de entrega
        """
        pass
    
    @abstractmethod
    def finish_delivery(self):
        """""
        Finaliza o processo de entrega
        """
        pass
    
    @abstractmethod
    def cancel_delivery(self, reason: str):
        """
        Cancela a entrega
        """
        pass
    
    @abstractmethod
    def status(self) -> str:
        """
        Retorna o status da entrega.
        """
        pass