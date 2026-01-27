
from .purchase import Purchase
from .distributor import Distributor
from ..abstracts.abstract_manager import AbstractManager
from ..mixins.authorization_mixin import AuthorizationMixin



class Manager(AuthorizationMixin, AbstractManager):
    def __init__(self, name="Gerente", registration="123"):
        super().__init__(name, registration)
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

    def ver_estoque(self, estoque):
        if not estoque:
            return "Estoque vazio."
        total_pallets = len(estoque)
        total_valor = sum(p.quantidade * p.preco_unitario for p in estoque)
        return f"Total de pallets: {total_pallets}, Valor total: R${total_valor:.2f}"

    def lista_clientes(self):
        return "Lista de clientes não implementada."

    def lista_vendedores(self):
        return "Lista de vendedores não implementada."

    def lista_motoristas(self):
        return "Lista de motoristas não implementada."
