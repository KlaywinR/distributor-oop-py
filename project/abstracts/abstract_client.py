from datetime import datetime, date, timedelta
from abc import abstractmethod, ABC

class AbstractClient(ABC):
    """
    Classe base que define o contrato para qualquer tipo de cliente do sistema.
    A mesma possui aplicações dos princípios solid:
    - SRP: A classe define apenas o comportamento  esperado do cliente sem a implementação de regras.
    - OCP: Novos tipos de clientes podem ser criados por herança.
    
    """
    
    @abstractmethod
    def buy(self, product, quantity_pallets, unit_value_pallet):
        pass

    @abstractmethod
    def client_category(self):
        pass
    
    @abstractmethod
    def summary_client(self):
        pass
    
    @abstractmethod
    def volume_discount(self, quantity_pallets):
        pass

    @abstractmethod
    def add_loyalty_points(self, buy_value):
        pass
    
    @abstractmethod
    def claim_points(self):
        pass
    
    @abstractmethod
    def check_promotion(self, buy_value):
        pass
    
    @abstractmethod
    def rate_service(self, stars):
        pass
    
    @abstractmethod 
    def client_status(self):
        pass