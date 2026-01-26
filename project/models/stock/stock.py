
from .stock_base import BaseStock
from ..mixins.movement_mixin import MovementMixin
from .stock_item import StockItem
from products.product import Product


class Stock(BaseStock, MovementMixin):
    def __init__(self, total_capacity: int, responsible: str, name: str):
        super().__init__(total_capacity)
        self._responsible = responsible
        self._movement_history = []
        self._status = "Vazio"
        self._name = name 
        
    @property
    def responsible(self):
        return self._responsible
    
    @responsible.setter
    def responsible(self, name: str):
        self._responsible = name 
        
    def add_pallet(self, product: Product, pallets: int):
        
        if not product.is_active():
            raise ValueError("Informação do Sistema: O produto está inativo")
        if product.is_expired():
            raise PermissionError("Informação do Sistema: O produto está vencido")
        
        for item in self._pallet_list:
            if item.product.barcode == product.barcode:
                item.pallets += pallets
                self.register_movement(f"Entrada de {pallets} pallets do produto {product.name}")
             
                self._update_status()
                return 
        
        self._pallet_list.append(StockItem(product,pallets))   
        self.register_movement( f"Entrada de {pallets} pallets do produto {product.name}")
        
        self._update_status()
          
    def del_pallet(self,product: Product, pallets: int):
        for item in self._pallet_list:
            if item.product.barcode == product.barcode:
                if pallets > item.pallets:
                    raise ValueError("Informação do Sistema: Estoque insuficiente")
                
                item.pallets -= pallets
                self.register_movement(f"Informação do Sistema: Removidos {pallets} pallets do produto {product.name}")
                    
                if item.pallets == 0:
                    self._pallet_list.remove(item)
                
                self._update_status()
                return
            raise ValueError("O produto não foi encontrado no estoque")
    
    #pallet listaddo no atacado
    def list_pallets(self) -> list[StockItem]:
        return self._pallet_list.copy()
    
    def search_product_id(self, product_id):
        return next(
            (item for item in self._pallet_list if item.product.barcode == product_id),
            None
        )
    
    def total_stock_value(self):
        return sum(item.total_value() for item in self._pallet_list)
        
    #built ins
    def view_status(self):
        return self._status
    
    def _update_status(self):
        total_pallets = sum(item.pallets for item in self._pallet_list)
        if total_pallets == 0:
            self._status = "VAZIO"
        elif total_pallets < self._total_capacity * 0.3:
            self._status = "BAIXO" 
        else:
            self._status = "CHEIO"
              
    def __str__(self):
        return (
            f"-- Informações Gerais do Estoque --\n"
            f"Estoque: {self._name}\n"
            f"Responsável(a): {self.responsible}\n"
            f"Status: {self._status}\n"
            f"Total Pallets: {sum(i.pallets for i in self._pallet_list)}\n"
            f"Valor total do estoque: {self.total_stock_value():.2f}"
        )
            