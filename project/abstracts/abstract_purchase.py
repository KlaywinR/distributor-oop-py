
from project.interfaces.interface_purchase import InterfacePurchase
from abc import ABC
from datetime import datetime

class AbstractPurchase(InterfacePurchase, ABC):
    def __init__(self, client, seller, product, quantity_pallets):
        self._client = client
        self._seller = seller
        self._product = product
        self._quantity_pallets = quantity_pallets
        self._date = datetime.now()
        self._status = "PENDING"
        self._total_value = 0.0
        