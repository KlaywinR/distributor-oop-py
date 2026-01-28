
from .purchase import Purchase
from .distributor import Distributor
from ..abstracts.abstract_manager import AbstractManager
from ..mixins.authorization_mixin import AuthorizationMixin


class Manager(AuthorizationMixin, AbstractManager):
    """ Representa o gerente do sistema."""
    
    def __init__(self, name="Gerente", registration="123"):
        """ Inicializa o gerente com nome e matrícula."""
        super().__init__(name, registration)
        
    def approve_purchase(self, purchase: Purchase):    
       if purchase.total_value > 50000:
           self._authorize("INFORMAÇÃO DO SISTEMA: Compra de Alto Valor")
           purchase.mark_as_approved()
       
    def approve_discount(self, client, percentage):
        """"
           - Descontos de até 15% são aprovados automaticamente.
            - Descontos acima de 15% são negados.
        """
        if percentage <= 15:
            self._authorize("INFORMAÇÃO DO SISTEMA: Desconto padrão aprovado")
            if hasattr(client, "apply_discount"):
                client.apply_discount(percentage)
        else: 
            raise PermissionError("INFORMAÇÃO DO SISTEMA: Desconto acima do limite permitido")
    
    def request_report(self, distributor: Distributor):
        """"
        O relatório inclui:
            - Faturamento total
            - Quantidade de clientes ativos
        """
        
        return {
            "faturamento": distributor.total_revenue(),
            "clientes_ativos": len(distributor.active_clients())
        }
        
    def manage_employee(self, employee, action: str):
        """
          - PROMOTE: promove o funcionário
          - DISMISS: demite o funcionário

        """
        if action  == "PROMOTE" and hasattr(employee, "promote"):
            employee.promote()
        elif action == "DISMISS" and hasattr(employee, "dismiss"):
            employee.dismiss()

    def ver_estoque(self, estoque):
        """Visualiza o estoque"""
        if not estoque:
            return "Estoque vazio."
        total_pallets = len(estoque)
        total_valor = sum(p.quantidade * p.preco_unitario for p in estoque)
        return f"Total de pallets: {total_pallets}, Valor total: R${total_valor:.2f}"

    def lista_clientes(self):
        """Retorna a lista de clientes cadastrados no sistema"""
        return "Lista de clientes não implementada."

    def lista_vendedores(self):
        """Retorna a lista de vendedores no sistema."""
        return "Lista de vendedores não implementada."

    def lista_motoristas(self):
        """Retorna a lista de motoristas no sistema."""
        return "Lista de motoristas não implementada."
