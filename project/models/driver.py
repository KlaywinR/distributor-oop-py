
from ..mixins.avaibility_mixin import AvailabilityMixin
from ..abstracts.abstract_driver import AbstractDriver
from datetime import date

class Driver(AvailabilityMixin, AbstractDriver):
    
    MAX_OCCURRANCES = 5

    def __init__(self, id_driver, name, cpf, cnh_category, cnh_expiration,
                 max_capacity_pallets, region):
        
        self.__id_driver = id_driver
        self._name = name 
        self.__cpf = cpf
        self.__cnh_category =  cnh_category
        self.__cnh_expiration = cnh_expiration
        self._status  = "ATIVO"
        
        self.__max_capacity_pallets =  max_capacity_pallets
        self.__region = region
        
        self.__deliveries_assigned = []
        self.__routes_history = []
        self.__infractions = []
        self.__occurances = []
        self._score = 100
        
    @property
    def name(self):
        return self._name 
    
    @property
    def status(self):
        return self._status
    
    def cnh_is_valid(self) -> bool:
        return self.__cnh_expiration >= date.today()
    
    def can_operate(self) ->  bool:
        return (
            self._status == "ATIVO"
            and self.cnh_is_valid()
            and len(self.__occurances) < self.MAX_OCCURRANCES
        )
        
    def assign_delivery(self, delivery):
        if not self.can_operate():
            raise PermissionError("O motorista não pode operar")
        self.__deliveries_assigned.append(delivery)
          
    def accept_delivery(self, delivery):
        delivery.start_delivery()
                
    def reject_delivery(self):
        self.register_occurance("A entrega foi recusada")

    def complete_delivery(self, delivery):
        delivery.complete()
        self.__routes_history.append(delivery)
        
    def register_occurance(self, description):
        self.__occurances.append(description)
        self._update_score()
    
    def _update_score(self):
        self._score -= 10
        if self._score <= 50:
            self._block_driver()
    
    def _block_driver(self):
        self._status = "BLOQUEADO"
    
    def __len__(self):
        return len(self.__deliveries_assigned)
    
    def __str__(self):
        return f"Motorista: {self._name}, Status: {self._status}"