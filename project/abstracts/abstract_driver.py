
from abc import ABC, abstractmethod
    
class AbstractDriver(ABC):
    
    @abstractmethod
    def can_operate(self) -> bool:
        pass

    @abstractmethod
    def assign_delivery(self, delivery):
        pass
    
    @abstractmethod
    def complete_delivery(self, delivery):
        pass
