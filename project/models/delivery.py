

from ..mixins.delay_control_mixin import DelayControlMixin
from .abstract_delivery import AbstractDelivery
from datetime import datetime, timedelta


class Delivery(DelayControlMixin, AbstractDelivery):
    
    STATUS_PENDING = "PENDING"
    STATUS_ASSIGNED = "ASSIGNED"
    STATUS_IN_TRANSIT = "IN_TRANSIT"
    STATUS_DELIVERED = "DELIVERED"
    STATUS_DELAYED = "DELAYED"
    STATUS_CANCELED = "CANCELED"
    
    BASE_PRICE = 20.0
    PRICE_PER_KM = 2.5
    EXPRESS_FEE = 30.0
    DELAY_PENALTY = 15.0
    
    def __init__(self, id_delivery, estimated_hours, distance_km,id_vehicle,type_vehicle,status_vehicle,capacity_vehicle,express=False):
        super().__init__(id_delivery)
        self._estimated_time = datetime.now() + timedelta(hours= estimated_hours)
        self._receiver_name = None
        self._proof = None
        self._driver = None
        self._distance_km = distance_km
        self._express = express
        self._type_vehicle = type_vehicle
        self._id_vehicle = id_vehicle
        self._status_vehicle = status_vehicle
        self._capacity_vehicle = capacity_vehicle
        self._timeline = []
        self._register_event("Entrega Criada")
    
        
    @property
    def id_veiculo(self): 
        return self.__id_veiculo   
            
    @property
    def type(self): 
        return self.__type_vehicle
    
         
    @property
    def capacity(self): 
        return self.__id_vehicle   
            
    @property
    def status_vehicle(self): 
        return self.__status_vehicle
    
    def assign_driver(self, driver):
        if self._status != self.STATUS_PENDING:
            raise ValueError("O motorista só pode ser solicitado quando existir entregas pendentes..")
        self._driver = driver 
        self._status = self.STATUS_ASSIGNED
        self._register_event("Motorista Atribuido")
        
    def calculate_cost(self):
        cost = self.BASE_PRICE + self._distance_km * self.PRICE_PER_KM
        
        if self._express:
            cost += self.EXPRESS_FEE
        if self.is_delayed():
            cost += self.DELAY_PENALTY
        return round(cost, 2)
        
    def can_start(self) -> bool:
        return self._status == self.STATUS_ASSIGNED and self._driver is not None

    def can_finish(self) -> bool:
        return self._status == self.STATUS_IN_TRANSIT
    
    def can_cancel(self) -> bool:
        return self._status not in (self.STATUS_DELIVERED, self.STATUS_CANCELED)
    
    def is_active(self) -> bool:
        return self._status in (
            self.STATUS_ASSIGNED,
            self.STATUS_IN_TRANSIT,
            self.STATUS_DELAYED
        )
        
    def _register_event(self, description: str):
        self._timeline.append({
            "event": description,
            "date": datetime.now()
        })
        
    def get_timeline(self):
        return self._timeline
    
    def start_delivery(self):
      if not self.can_start():
          raise PermissionError("A entrega não pode ser inciada")
      
      self._status = self.STATUS_IN_TRANSIT
      self._started_at = datetime.now()
      self._register_event("Entrega Iniciada")
      self.notify_costumer("Sua encomenda saiu para a entrega")
      
    def finish_delivery(self):
      if not self.can_finish():
          raise PermissionError("Mensagem do Sistema: A entrega não pode ser finalizada!")
      
      self._status = self.STATUS_DELIVERED
      self._finished_at = datetime.now()
      self._register_event("Entrega Finalizada")
      self.notify_costumer("Entrega Realizada com sucesso!")
      
    def cancel_delivery(self, reason: str):
        if not self.can_cancel():
            raise PermissionError("A sua entrega não pode ser cancelada")

        self._status = self.STATUS_CANCELED
        self._register_occurance(reason)
        self._register_event("A sua entrega foi cancelada")
        self.notify_costumer(f"Entrega cancelada: {reason}")
        
    def notify_costumer(self, message: str):
        print(f"[CLIENTE] Entrega {self._id_delivey}: {message}")
        
    def __len__(self):
        return len(self._occurances)
    
    def __str__(self): 
        return (f"Veículo {self.__id_veiculo},- {self.__tipo} " f"({self.__placa}), Capacidade: {self.__capacidade}kg, " f"Status: {self.__status.value}, " f"Motorista: {self.__motorista.nome if self.__motorista else 'Nenhum'}")
