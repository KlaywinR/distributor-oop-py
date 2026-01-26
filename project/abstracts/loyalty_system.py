from abc import ABC, abstractmethod

class LoyaltySystem(ABC):
    
    @abstractmethod
    def claim_points(self):
        pass
    
    @abstractmethod
    def add_loyalty_points(self, buy_value):
        pass
    