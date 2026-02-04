from abc import ABC, abstractmethod

class InterfacePallet(ABC):

    @abstractmethod
    def add_products(self, quantity: int) -> None:
        """
        O pallet pode adicionar produtos
        """
        pass
    
    @abstractmethod
    def remove_products(self, quantity: int) -> None:
        """
        O pallet pode remover produtos
        """
        pass
    
    @abstractmethod
    def calculate_wheight(self) -> float:
        """
        Calculo do peso
        """
        pass
    
    @abstractmethod
    def is_full(self) -> bool:
        """
       Retorna se esta cheio de produtos.
        """
        pass
    
    @abstractmethod
    def is_empty(self)-> bool:
        """
       Retorna se esta vazio de produtos.
        """
        pass
