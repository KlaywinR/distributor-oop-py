from abc import ABC,  abstractmethod

class CustomerServiceInterface(ABC):
    
    @abstractmethod
    def attend_costumer(self, customer):
        pass
    
    @abstractmethod
    def respond_to_complaint(self, client):
        pass
