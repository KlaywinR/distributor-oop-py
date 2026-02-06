
from project.interfaces.distributor_interface import DistributorInterface
from abc import ABC
from models.stock.stock import Stock
    
class AbstractDistributor(DistributorInterface, ABC):
    
    def __init__(self, name: str, cnpj: str):
        """"
        Inicializa-se a distribuidora com nome e cnpj.
        """
        self._name = name 
        self._cnpj = cnpj
        self._clients = []
        self._employees = []
        self._stocks = [Stock]
        self._purchases = []
        self._deliveries =  []
    