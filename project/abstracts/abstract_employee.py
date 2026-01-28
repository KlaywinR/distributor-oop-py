from abc import ABC, abstractmethod
  
class AbstractEmployee(ABC):
    """
    A classe abstrata Employee é tida como base comum para todo tipo de funcionário.
    Logo, garante todas as regras de funcionamento, estrutura e comportamento. Onde, funciona sem a necessidade de instâncias diretas. 
    """
    
    @abstractmethod
    def register_entry(self):
        """
        Regra de registro de entrada do funcionário
        """
        pass
       
    @abstractmethod
    def register_exit(self):
        """
        Regra de registro da saída do funcionário
        """
        pass
    
    @abstractmethod
    def calculate_overtime(self, day_type="Normal"):
        """
        Cálculo matemático das horas extras, é levada em conta a atual jornada trabalhista de oito horas (8).
        """
        pass 
    
    @abstractmethod
    def request_vacation(self):
        """
        Pedido de férias por parte do funcionário
        """
        pass
    
    @abstractmethod
    def request_raise(self,percentage):
        """
        Pedido de aumento por parte do funcionário
        """
        pass
    
    @abstractmethod
    def status_employee(self):
        """
        Status do funcionário
        """
        pass