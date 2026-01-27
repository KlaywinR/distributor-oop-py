
from ..interfaces.delivery_interface import DeliveryInterface
from abc import abstractmethod, ABC
from datetime import datetime

class AbstractDelivery(DeliveryInterface, ABC):
    
    def __init__(self, id_delivery):
        self._id_delivery = id_delivery
        self._created_at = datetime.now()
        self._started_at = None
        self._finished_at = None
        self._status = "PENDING"
        self._occurrences = []
        
    def status(self) -> str:
        return self._status
    
    def _register_occurance(self, description: str):
        self._occurrences.append({
            "description": description,
            "date": datetime.now()
        })
    
    def get_occurrances(self):
        return self._occurrances  
    
    @abstractmethod
    def calculate_cost(self) -> float:
        pass
    
    @abstractmethod
    def notify_costumer(self, message: str):
        pass