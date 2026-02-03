

from ..mixins.delay_control_mixin import DelayControlMixin
from ..abstracts.abstract_delivery import AbstractDelivery
from datetime import datetime, timedelta


class Delivery(DelayControlMixin, AbstractDelivery):
    """
        - DelayControlMixin: controla atrasos e ocorrências.
        - AbstractDelivery: define a interface base de uma entrega.
    """
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
        self.estimated_time = datetime.now() + timedelta(hours= estimated_hours)
        self.driver = None
        self.express = express
        self.id_delivery = id_delivery
        self._distance_km = distance_km
        self._express = express
        self.type_vehicle = type_vehicle
        self.id_vehicle = id_vehicle
        self.status_vehicle = status_vehicle
        self.capacity_vehicle = capacity_vehicle
        self._timeline = []
        self._register_event("Entrega Criada")
    
        
    @property
    def id_veiculo(self): 
        """Retorna o identificador do veículo."""
        return self.id_vehicle  
            
    @property
    def type(self): 
        """Retorna o tipo do veículo utilizado na entrega."""
        return self.type_vehicle
    
         
    @property
    def capacity(self): 
        """Retorna a capacidade do veículo."""
        return self.id_vehicle   
            
    @property
    def status_vehicle(self): 
        """Retorna o status atual do veículo."""
        return self._status_vehicle
    
    @status_vehicle.setter
    def status_vehicle(self, value):
        self._status_vehicle = value
    
    def assign_driver(self, driver):
        """
        Atribui um motorista à entrega.
            - A atribuição só é permitida quando a entrega estiver pendente.        
        """
        if self._status != self.STATUS_PENDING:
            raise ValueError("O motorista só pode ser solicitado quando existir entregas pendentes..")
        self.driver = driver 
        self.status = self.STATUS_ASSIGNED
        self._register_event("Motorista Atribuido")
        
    def calculate_cost(self):
        """
          Calcula o custo total da entrega.
            - Valor base
            - Distância percorrida
            - Taxa de entrega expressa
            - Penalidade por atraso
        """
        cost = self.BASE_PRICE + self._distance_km * self.PRICE_PER_KM
        
        if self._express:
            cost += self.EXPRESS_FEE
        if self.is_delayed():
            cost += self.DELAY_PENALTY
        return round(cost, 2)
        
    def can_start(self) -> bool:
        """Verifica se a entrega pode ser iniciada."""
        return self.status == self.STATUS_ASSIGNED and self.driver is not None

    def can_finish(self) -> bool:
        """Verifica se a entrega pode ser finalizada."""
        return self.status == self.STATUS_IN_TRANSIT
    
    def can_cancel(self) -> bool:
        """Verifica se a entrega pode ser cancelada"""
        return self.status not in (self.STATUS_DELIVERED, self.STATUS_CANCELED)
    
    def is_active(self) -> bool:
        """Verifica se a entrega está ativa no sistema."""
        return self._status in (
            self.STATUS_ASSIGNED,
            self.STATUS_IN_TRANSIT,
            self.STATUS_DELAYED
        )
        
    def _register_event(self, description: str):
        """Registra um evento na linha do tempo da entrega."""
        self._timeline.append({
            "event": description,
            "date": datetime.now()
        })
        
    def get_timeline(self):
        """Retorna o histórico de eventos da entrega."""
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
        """Cancela a entrega informando o motivo."""
        if not self.can_cancel():
            raise PermissionError("A sua entrega não pode ser cancelada")

        self._status = self.STATUS_CANCELED
        self._register_occurance(reason)
        self._register_event("A sua entrega foi cancelada")
        self.notify_costumer(f"Entrega cancelada: {reason}")
        
    def notify_costumer(self, message: str):
        print(f"[CLIENTE] Entrega {self.id_delivery}: {message}")
        
    def __len__(self):
        """Retorna a quantidade de ocorrencias registradas"""
        return len(self._occurances)
    
    def __str__(self): 
        """Representação textual da entrega"""
        return (
            f"Veículo {self.id_vehicle},{self.type_vehicle}"
            f"Capacidade: {self.capacity_vehicle}kg, Status: {self.status_vehicle}, "
            f"Motorista: {self.driver if self.driver else 'Nenhum'}")
