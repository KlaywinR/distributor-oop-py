
from abc import ABC, abstractmethod

class Promocional(ABC):
    """
     Classe abstrata base para objetos que podem receber promoções.
    """  
    @abstractmethod
    def add_promotion(self, new_price: float) -> None:
        """
        Aplica uma promoção alterando o preço do item.
        """
        pass
    
    @abstractmethod
    def remove_promotion(self):
        """
        Remove a promoção aplicada ao item.
        """
        pass
    
    @abstractmethod
    def has_promotion(self)-> bool:
        """
        Verifica se o item possui promoção ativa.
        """
        pass
    
    @abstractmethod
    def current_price(self) -> float:
        """"
        Retorna o preço atual do item.
        """
        pass