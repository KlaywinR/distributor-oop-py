
from abc import ABC, abstractmethod
    
class AbstractDriver(ABC):
    """
    Classe abstrata base para representar um motorista.
    """
    
    @abstractmethod
    def can_operate(self) -> bool:
        """
        Verifica se o motorista está apto para operar.
        """
        pass

    @abstractmethod
    def assign_delivery(self, delivery):
        """
        Atribui uma entrega ao motorista.
        """
        pass
    
    @abstractmethod
    def complete_delivery(self, delivery):
        """
        Finaliza uma entrega atribuída ao motorista.
        """
        pass
