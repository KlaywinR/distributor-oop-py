from project.models.product.product import Product

class StockItem:
    """
    Representa um item armazenado no estoque.
    Cada StockItem associa um produto a uma quantidade de pallets,
    permitindo cálculos relacionados a unidades e valor total em estoque.
    """
    def __init__(self, product: Product, pallets:int):
        """Itens de um Estoque Y"""
        self.product = product
        self.pallets = pallets
    
    def total_units(self) -> int:
        """Calcula o total de unidades do produto no estoque."""
        return self.pallets * self.product.units_per_pallet
    
    def total_value(self):
        """ Calcula o valor total do item em estoque."""
        return self.total_units() * self.product.current_price()