from abc import ABC,  abstractmethod

class CustomerServiceInterface(ABC):
    
    @abstractmethod
    def attend_costumer(self, customer):
        """""
        Atendimento ao cliente.
        """
        pass
    
    @abstractmethod
    def respond_to_complaint(self, client):
        """
        Responder reclamação do cliente.
        """
        pass
