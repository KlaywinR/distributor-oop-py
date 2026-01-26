from products.product import Product

class StockItem:
    def __init__(self, product: Product, pallets:int):
        self.product = product
        self.pallets = pallets
    
    def total_units(self) -> int:
        return self.pallets * self.product.units_per_pallet
    
    def total_value(self):
        return self.total_units() * self.product.current_price()