
from project.interfaces.stock_interface import StockInterface
from project.models.stock.stock_item import StockItem

class BaseStock(StockInterface):
    def __init__(self, total_capacity: int):
        self._total_capacity = total_capacity
        self._pallet_list: list[StockItem] = []