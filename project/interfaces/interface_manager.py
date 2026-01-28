
from abc import abstractmethod, ABC

class InterfaceManager(ABC):
    
    @abstractmethod
    def approve_purchase(self, purchase):
        """
        Aprova uma compra com base no valor da compra.
        """
        pass
    
    @abstractmethod
    def approve_discount(self, discount):
        """
        Aprova o desconto
        """
        pass
    
    @abstractmethod
    def request_report(self, distributor):
        """
        Retorna relatorios de distribuidora
        """
        pass
    
    @abstractmethod
    def manage_employee(self, employee, action: str):
        """
        Realiza ações de gestão sobre um funcionário.
        """
        pass