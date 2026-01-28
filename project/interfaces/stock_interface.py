from abc import ABC, abstractmethod
from project.models.product.product import Product

class StockInterface(ABC):
    
    @abstractmethod
    def add_pallet(self, product: Product, quantity: int):
        """"
        Adiciona paletes no estoque
        """
        pass
    
    @abstractmethod
    def del_pallet(self, product: Product, quantity: int):
        """"
        Deleta paletes no estoque
        """
        pass
    
    @abstractmethod
    def view_status(self):
        """"
        Visualiza paletes no estoque
        """
        pass
    
    @abstractmethod
    def total_stock_value(self):
        """"
        Retorna o valor do estoque
        """
        pass
    
    @abstractmethod
    def list_pallets(self):
        """"
        Lista a quantidade de pallets
        """
        pass
    