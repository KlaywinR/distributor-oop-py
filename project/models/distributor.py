
from ..mixins.audit_mixin import AuditMixin
from ..mixins.report_mixin import ReportMixin
from .abstract_distributor import AbstractDistributor

class Distributor(ReportMixin, AuditMixin, AbstractDistributor):
    
    def register_client(self, client):
        self._clients.append(client)
        self._log(f"Cliente {client.name} registrado com sucesso!")
        
    def register_employee(self, employee):
        self._employees.append(employee)
        self._log(f"Funcionário {employee.name} registrado com sucesso!")
        
    def register_stock(self, stock):
        self._stocks.append(stock)
        self._log(f"Estoque {stock._name} registrado com sucesso!")
        
    def process_purchase(self, purchase):
        purchase.finalize_purchase()
        self._purchases.append(purchase)
        self._log("Compra registrada com sucesso!")
        
    def dispatch_delivery(self, delivery):
        delivery.start_delivery()
        self._deliveries.append(delivery)
        self._log("Entrega despachada com sucesso!")
        
#! met privado:
    def __validate_employee(self, employee):
        return hasattr(employee, "register_entry")
    
    def __validate_client(self, client):
        return hasattr(client, "buy")
    
#! conc. duck
    def notify(self, entity):
        entity.receive_notification("Informação do Sistema: O Sistema foi atualizado")
        
    #! built - ins
    
    def __str__(self):
          return f"Distribuidora {self._name} | Clientes: {len(self._clients)}"
#? ver os metodos privados 