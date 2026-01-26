

from abc import ABC, abstractmethod
from products.product import Product

class StockInterface(ABC):
    
    @abstractmethod
    def add_pallet(self, product: Product, quantity: int):
        pass
    
    @abstractmethod
    def del_pallet(self, product: Product, quantity: int):
        pass
    
    @abstractmethod
    def view_status(self):
        pass
    
    @abstractmethod
    def total_stock_value(self):
        pass
    
    @abstractmethod
    def list_pallets(self):
        pass
    