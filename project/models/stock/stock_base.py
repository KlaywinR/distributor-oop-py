
from project.interfaces.stock_interface import StockInterface
from project.models.stock.stock_item import StockItem

class BaseStock(StockInterface):
    """ Classe base responsável pelo gerenciamento do estoque de pallets."""
    def __init__(self, total_capacity: int):
        """Inicializa o estoque base com uma capacidade máxima definida."""
        self._total_capacity = total_capacity
        self._pallet_list: list[StockItem] = []