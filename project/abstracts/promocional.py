
from abc import ABC, abstractmethod

class Promocional(ABC):  
    
    @abstractmethod
    def add_promotion(self, new_price: float) -> None:
        pass
    
    @abstractmethod
    def remove_promotion(self):
        pass
    
    @abstractmethod
    def has_promotion(self)-> bool:
        pass
    
    @abstractmethod
    def current_price(self) -> float:
        pass