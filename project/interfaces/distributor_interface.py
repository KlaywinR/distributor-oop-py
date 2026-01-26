
from abc import ABC,abstractmethod

class DistributorInterface(ABC):
#! posssui princípio dip + abstração + interface
    
    @abstractmethod
    def register_client(self, client):
        pass
    
    @abstractmethod
    def register_employee(self, employee):
        pass
    
    @abstractmethod
    def register_stock(self, stock):
        pass
    
    @abstractmethod
    def process_purchase(self, purchase):
        pass
    
    @abstractmethod
    def dispatch_delivery(self, delivery):
        pass
    