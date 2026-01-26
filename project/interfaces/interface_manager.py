
from abc import abstractmethod, ABC

class InterfaceManager(ABC):
    
    @abstractmethod
    def approve_purchase(self, purchase):
        pass
    
    @abstractmethod
    def approve_discount(self, discount):
        pass
    
    @abstractmethod
    def request_report(self, distributor):
        pass
    
    @abstractmethod
    def manage_employee(self, employee, action: str):
        pass