
from project.mixins.audit_mixin import AuditMixin
from project.mixins.report_mixin import ReportMixin
from project.abstracts.abstract_distributor import AbstractDistributor

class Distributor(ReportMixin, AuditMixin, AbstractDistributor):
    
    def register_client(self, client):
        """Registra um cliente"""
        self._clients.append(client)
        self._log(f"Cliente {client.name} registrado com sucesso!")
        
    def register_employee(self, employee):
        """Registra um funcionario"""
        self._employees.append(employee)
        self._log(f"Funcionário {employee.name} registrado com sucesso!")
        
    def register_stock(self, stock):
        """Registra um estoque"""
        self._stocks.append(stock)
        self._log(f"Estoque {stock._name} registrado com sucesso!")
        
    def process_purchase(self, purchase):
        """Processa uma compra"""
        purchase.finalize_purchase()
        self._purchases.append(purchase)
        self._log("Compra registrada com sucesso!")
        
    def dispatch_delivery(self, delivery):
        """Inicia a entrega"""
        delivery.start_delivery()
        self._deliveries.append(delivery)
        self._log("Entrega despachada com sucesso!")
        
    def __validate_employee(self, employee):
        """Valida o funcionário"""
        return hasattr(employee, "register_entry")
    
    def __validate_client(self, client):
        """Valida o cliente"""
        return hasattr(client, "buy")
    
    def notify(self, entity):
        """
        Envia uma notificação para qualquer entidade compatível.
        - Duck Typing: qualquer objeto que possua o método `receive_notification` pode ser usado como parametro 
        independente da classe ou herança.
        """
        entity.receive_notification("Informação do Sistema: O Sistema foi atualizado")
   
    def __str__(self):
        """Retorna representação textual"""
        return f"Distribuidora {self._name} | Clientes: {len(self._clients)}"
