
from project.interfaces.delivery_interface import DeliveryInterface
from abc import abstractmethod, ABC
from datetime import datetime

class AbstractDelivery(DeliveryInterface, ABC):
    """
    Representa uma classe para entrega no sistema.
    """
    
    def __init__(self, id_delivery):
        """"
        Entrega com identificador padrão e dados.
        """
        self.id_delivery = id_delivery
        self._created_at = datetime.now()
        self._started_at = None
        self._finished_at = None
        self._status = "PENDING"
        self._occurrences = []
        
    def status(self) -> str:
        """
        Retorna o status da entrega.
        """
        return self._status
    
    def _register_occurance(self, description: str):
        """
        Registra uma ocorrência relacionada a entrega do pallet.
        """
        self._occurrences.append({
            "description": description,
            "date": datetime.now()
        })
    
    def get_occurrences(self):
        """""
        Retorna a lista de ocorrências registradas.
        """
        return self._occurrences  
    
    @abstractmethod
    def calculate_cost(self) -> float:
        """
        Calcula o custo da entrega.
        """
        pass
    
    @abstractmethod
    def notify_costumer(self, message: str):
        """
        Notifica o cliente sobre a entrega.
        """
        pass