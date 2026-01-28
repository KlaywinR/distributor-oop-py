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
        """
        O cliente compra o pallet.
        """
        pass

    @abstractmethod
    def client_category(self):
        """
        Retorna a Categoria do cliente conforme o valor da compra.
        """
        pass
    
    @abstractmethod
    def summary_client(self):
        """
        Retorna a resumo do cliente.
        """
        pass
    
    @abstractmethod
    def volume_discount(self, quantity_pallets):
        """
        Retorna o desconto por volume baseado na quantidade de pallets.
        """
        pass

    @abstractmethod
    def add_loyalty_points(self, buy_value):
        """
        Adiciona pontos fidelidade à conta do cliente.
        """
        pass
    
    @abstractmethod
    def claim_points(self):
        """
        Reclama os pontos acumulativos.
        """
        pass
    
    @abstractmethod
    def check_promotion(self, buy_value):
        """
        Checagem de promoção pelo cliente.
        """
        pass
    
    @abstractmethod
    def rate_service(self, stars):
        """
        O cliente avalia o serviço feito.
        """
        pass
    
    @abstractmethod 
    def client_status(self):
        """
        Retorna o status do cliente.
        """
        pass