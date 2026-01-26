
from datetime import date
from interfaces.pallet_interface import InterfacePallet


class AbstractPallet(InterfacePallet):
    """
    Lógica base para a classe Pallet
    """
    def __init__(self, id_pallet, product,max_capacity, max_wheight):
        self._id_pallet = id_pallet
        self._product = product
        self._max_capacity = max_capacity
        self._max_wheight = max_wheight
        self._current_weight = 0.0
        self._quantity_products =  0.0
        self._input_date = date.today()
       