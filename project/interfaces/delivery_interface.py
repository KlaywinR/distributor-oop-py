
from abc import ABC, abstractmethod

class DeliveryInterface(ABC):
    
    @abstractmethod
    def start_delivery(self):
        pass
    
    @abstractmethod
    def finish_delivery(self):
        pass
    
    @abstractmethod
    def cancel_delivery(self, reason: str):
        pass
    
    @abstractmethod
    def status(self) -> str:
        pass