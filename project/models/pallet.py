
from .abstract_pallet import AbstractPallet
from ..mixins.status_mixin import StatusMixin

class Pallet(StatusMixin, AbstractPallet):
    def __init__(self, id_pallet, product, max_capacity, max_wheight, location_in_stock):
        super().__init__(id_pallet, product, max_capacity, max_wheight)
        self._location_in_stock = location_in_stock
        self._status = "Ativo"
    
    @property
    def quantity_products(self) -> int:
        return self._quantity_products
    
    @quantity_products.setter
    def quantity_products(self, value) -> int:
        if value < 0:
            raise ValueError("Mensagem do Sistema: A quantidade inválida")
        self._quantity_products = value
        
    @property
    def location_in_stock(self) -> str:
        return self._location_in_stock 
    
    @location_in_stock.setter
    def location_in_stock(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("Mensagem do Sistema: Localização Inválida")
        self._location_in_stock = value
    
    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, value: str) -> None:
        allowed_status = {"Ativo", "Bloqueado", "Shipped"}
        if value not in allowed_status:
            raise ValueError(f"Mensagem do Sistema: Status Inválido {value}")
        self._status = value
      
    @property
    def current_wheight(self) -> float:
        return self._current_weight
    
    @current_wheight.setter
    def current_wheight(self, value: float) -> None:
        if value < 0:
            raise ValueError("Mensagem do Sistema: O atual peso não pode ser negativo")
        if value > self._max_wheight:
            raise ValueError("Mensagem do Sistema: O peso atual excede o limite do pallet")
        self._current_weight = value 
         
    def add_products(self, quantity: int) -> None:
       if quantity <= 0:
           raise ValueError("Mensagem do Sistema: A quantidade inválida")
       if self._quantity_products + quantity > self._max_capacity:
           raise ValueError("Mensagem do Sistema: A capacidade mínima excedida")
       
       self._quantity_products += quantity
       self._current_weight = self.calculate_wheight()
       
    def remove_products(self, quantity: int)-> None:
       if quantity <= 0:
           raise ValueError("Mensagem do Sistema: A quantidade inválida")
       
       if quantity > self._quantity_products:
           raise ValueError("Mensagem do Sistema: Quantidade Insuficiente no Pallet")
       
       self._quantity_products -= quantity
       self._current_weight = self.calculate_wheight()
       
    def calculate_wheight(self) -> float:
        return self._quantity_products * self._product._wheight_per_unit
    
    def is_full(self) -> bool:
        return self._quantity_products == self._max_capacity
    
    def is_empty(self) -> bool:
        return self._quantity_products == 0
    
    def __str__(self) -> str:
        return (
            f"Pallet: {self._id_pallet}"
            f"Produto: {self._product}"
            f"Quantidade: {self._quantity_products}"
            f"Peso do Pallet: {self._current_weight:.2f} quilos"
            f"Status do Pallet: {self._status}"
        )