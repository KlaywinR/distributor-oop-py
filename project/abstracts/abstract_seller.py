from abc import ABC, abstractmethod

class AbstractSeller(ABC):
    
    @abstractmethod
    def make_sale(self, costumer, product, quantity):
        pass
    
    @abstractmethod
    def calculate_comissions(self):
        pass
