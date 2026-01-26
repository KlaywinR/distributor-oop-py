
from abc import ABC, abstractmethod

class InterfacePallet(ABC):
    """
    Define tudo o que o pallet deve saber fazer.
    """
    
    @abstractmethod
    def add_products(self, quantity: int) -> None:
        pass
    
    @abstractmethod
    def remove_products(self, quantity: int) -> None:
        pass
    
    @abstractmethod
    def calculate_wheight(self) -> float:
        pass
    
    @abstractmethod
    def is_full(self) -> bool:
        pass
    
    @abstractmethod
    def is_empty(self)-> bool:
        pass
