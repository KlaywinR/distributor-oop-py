
from ..mixins.avaibility_mixin import AvailabilityMixin
from ..abstracts.abstract_driver import AbstractDriver
from datetime import date
from .employee import Employee

class Driver(Employee, AvailabilityMixin, AbstractDriver):
    """
        - AvailabilityMixin: fornece controle de disponibilidade.
        - AbstractDriver: define a interface base de um motorista.
    """
    MAX_OCCURRANCES = 5

    def __init__(self, cpf,id_employee,name,shift, salary, departament, status_employee, admission_date, contract_type, region,  position, meta_monthly, overtime, hours_worked, id_driver, cnh_category, cnh_expiration, 
                 max_capacity_pallets):
        super().__init__(
            name="Klaywin R A Dias",
            shift=shift,
            cpf=cpf,
            salary=salary,
            id_employee=id_employee,
            departament=departament,
            status_employee=status_employee,
            admission_date=admission_date,
            contract_type=contract_type,
            position=position,
            meta_monthly=meta_monthly,
            overtime=overtime,
            hours_worked=hours_worked,
            region=region
            
        )
       
        self.cnh_category = cnh_category
        self.__cnh_expiration = cnh_expiration
        self.__max_capacity_pallets = max_capacity_pallets
        self.__region = region
        self._score = 100
        self._status = "ATIVO"
        self.__deliveries_assigned = []
        self.__routes_history = []
        self.__infractions = []
        self.__occurances = []
        self._id_driver = id_driver
       
    def cnh_is_valid(self) -> bool:
        """ Verifica se a CNH do motorista está válida."""
        return self.__cnh_expiration >= date.today()
    
    def can_operate(self) ->  bool:
        """
            - Status ativo
            - CNH válida
            - Número de ocorrências abaixo do limite máximo
        """
        return (
            self._status == "ATIVO"
            and self.cnh_is_valid()
            and len(self.__occurances) < self.MAX_OCCURRANCES
        )
           
    def assign_delivery(self, delivery):
        """ Atribui uma entrega ao motorista."""
        if not self.can_operate():
            raise PermissionError("O motorista não pode operar")
        self.__deliveries_assigned.append(delivery)
        
    def accept_delivery(self, delivery):
        """O motorista aceita a entrega a ser feita"""
        delivery.start_delivery()
                
    def reject_delivery(self):
        """O motorista rejeia a entrega a ser feita"""
        self.register_occurance("A entrega foi recusada")

    def complete_delivery(self, delivery):
        """O motorista completa a entrega que lhe foi atribuido"""
        delivery.complete()
        self.__routes_history.append(delivery)
        
    def register_occurance(self, description: str):
        """Registra uma ocorrência."""
        self.__occurances.append(description)
        self._update_score()
        
    def _update_score(self):
        """
        A cada ocorrência, a pontuação é reduzida.
        Caso atinja o limite mínimo, o motorista é bloqueado.
        """
        self._score -= 10
        if self._score <= 50:
            self._block_driver()
            
    def _block_driver(self):
        """Bloqueia o motorista"""
        self._status = "BLOQUEADO"
        
    @property
    def name(self):
        """Retorna o nome do motorista"""
        return self._name 
    
    @property
    def status(self):
        """Retorna o  status do motorista"""
        return self._status
    
    def __len__(self):
        """ Retorna a quantidade de entregas atribuídas ao motorista."""
        return len(self.__deliveries_assigned)
       
    def __str__(self):
        return (
            f"Motorista: {self.name} | "
            f"Status: {self._status} | "
            f"CNH: {self.cnh_category} | "
            f"Ocorrências: {len(self.__occurances)} | "
            f"Score: {self._score}"
        )