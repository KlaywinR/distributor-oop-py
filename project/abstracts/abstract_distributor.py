
from .distributor_interface import DistributorInterface
from abc import ABC
    
class AbstractDistributor(DistributorInterface, ABC):
    
    def __init__(self, name: str, cnpj: str):
        self._name = name 
        self._cnpj = cnpj
        self._clients = []
        self._employees = []
        self._stocks = []
        self._purchases = []
        self._deliveries =  []
    