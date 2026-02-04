
from datetime import date

class Pallet:
    """Representação do Pallet"""
    def __init__(self, name, quantity, price, valid):
        self.name = name
        self.quantity = quantity
        self.preco_unitario = price
        self.valid = valid
        self.promotional_price = None
    
    def is_active(self):
        """ Verifica se o pallet está ativo com base na validade do produto."""
        return self.validade >= date.today()
    
    @property
    def quantity_products(self) -> int:
        """ Retorna a quantidade atual de produtos no pallet."""
        return self._quantity_products
    
    @quantity_products.setter
    def quantity_products(self, value) -> int:
        """Define a quantidade de produtos no pallet."""
        if value < 0:
            raise ValueError("Mensagem do Sistema: A quantidade inválida")
        self._quantity_products = value
        
    @property
    def location_in_stock(self) -> str:
        """
        Retorna a localização do pallet no estoque.
        """
        return self._location_in_stock  
    
    @location_in_stock.setter
    def location_in_stock(self, value: str) -> None:
        """ Define a localização do pallet no estoque."""
        if not value or not isinstance(value, str):
            raise ValueError("Mensagem do Sistema: Localização Inválida")
        self._location_in_stock = value
    
    @property
    def status(self) -> str:
        """Retorna o status atual do pallet"""
        return self._status
    
    @status.setter
    def status(self, value: str) -> None:
        """
        Define o status do pallet.
        Status permitidos:
        - Ativo
        - Bloqueado
        - Shipped
        """
        allowed_status = {"Ativo", "Bloqueado", "Shipped"}
        if value not in allowed_status:
            raise ValueError(f"Mensagem do Sistema: Status Inválido {value}")
        self._status = value
      
    @property
    def current_wheight(self) -> float:
        """Retorna o peso atual do pallet."""
        return self._current_weight
    
    @current_wheight.setter
    def current_wheight(self, value: float) -> None:
        """Define o peso atual do pallet."""
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
        """ Calcula o peso total do pallet com base na quantidade de produtos"""
        return self._quantity_products * self._product._wheight_per_unit
    
    def is_full(self) -> bool:
        """ Verifica se o pallet está com capacidade máxima."""
        return self._quantity_products == self._max_capacity
    
    def is_empty(self) -> bool:
        """Verifica se o pallet está vazio."""
        return self._quantity_products == 0
    
    def __str__(self) -> str:
        """Representação Textual"""
        return (
            f"Pallet: {self._id_pallet}"
            f"Produto: {self._product}"
            f"Quantidade: {self._quantity_products}"
            f"Peso do Pallet: {self._current_weight:.2f} quilos"
            f"Status do Pallet: {self._status}"
        )