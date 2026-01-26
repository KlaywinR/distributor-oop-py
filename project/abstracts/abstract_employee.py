from abc import ABC, abstractmethod
  
class AbstractEmployee(ABC):
    """
    A classe abstrata Employee é tida como base comum para todo tipo de funcionário.
    Logo, garante todas as regras de funcionamento, estrutura e comportamento. Onde, funciona sem a necessidade de instâncias diretas. 
    """
    
    @abstractmethod
    def register_entry(self):
        pass
    
    """
    Regra de registro da saída do funcionário
    """
    @abstractmethod
    
    def register_exit(self):
        pass
    
    """
    Regra do cálculo matemático das horas extras do funcionário, é levada em conta a atual jornada trabalhista de oito horas (8).
    """
    @abstractmethod
    def calculate_overtime(self, day_type="Normal"):
        pass 
    
    @abstractmethod
    def request_vacation(self):
        pass
    
    @abstractmethod
    def request_raise(self,percentage):
        pass
    
    @abstractmethod
    def status_employee(self):
        pass