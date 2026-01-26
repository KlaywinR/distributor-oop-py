
from abc import ABC, abstractmethod
            
class InterfacePurchase(ABC):
    
    @abstractmethod
    def calculate_total(self):
        pass
    
    @abstractmethod
    def finalize_purchase(self):
        pass
    
    @abstractmethod
    def cancel_purchase(self):
        pass
    
    @abstractmethod
    def reserve_pallets(self):
        pass
    