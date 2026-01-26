

from ..mixins.authorization_mixin import AuthorizationMixin
from .abstract_manager import AbstractManager
from models.purchase import Purchase
from models.distributor import Distributor


class Manager(AuthorizationMixin, AbstractManager):
   
    def approve_purchase(self, purchase: Purchase):
       if purchase.total_value > 50000:
           self._authorize("INFORMAÇÃO DO SISTEMA: Compra de Alto Valor")
           purchase.mark_as_approved()
       
    def approve_discount(self, client, percentage):
        if percentage <= 15:
            self._authorize("INFORMAÇÃO DO SISTEMA: Desconto padrão aprovado")
            if hasattr(client, "apply_discount"):
                client.apply_discount(percentage)
        else: 
            raise PermissionError("INFORMAÇÃO DO SISTEMA: Desconto acima do limite permitido")
    
    def request_report(self, distributor: Distributor):
        return {
            "faturamento": distributor.total_revenue(),
            "clientes_ativos": len(distributor.active_clients())
        }
        
    def manage_employee(self, employee, action: str):
        if action  == "PROMOTE" and hasattr(employee, "promote"):
            employee.promote()
        elif action == "DISMISS" and hasattr(employee, "dismiss"):
            employee.dismiss()

    
