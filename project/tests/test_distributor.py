# Mocks das dependências
class AuditMixin:
    def _log(self, message: str):
        print(f"[AUDITORIA]: {message}")

class ReportMixin:
    def generate_report(self):
        return "Relatório gerado com sucesso!"

class AbstractDistributor:
    def __init__(self, name):
        self._name = name
        self._clients = []
        self._employees = []
        self._stocks = []
        self._purchases = []
        self._deliveries = []

# Mock Client
class Client:
    def __init__(self, name):
        self.name = name
    def buy(self):
        print(f"Cliente {self.name} realizou uma compra.")
    def receive_notification(self, msg):
        print(f"Cliente {self.name} recebeu notificação: {msg}")

# Mock Employee
class Employee:
    def __init__(self, name):
        self.name = name
    def register_entry(self):
        print(f"Funcionário {self.name} registrou entrada.")

# Mock Stock
class Stock:
    def __init__(self, name):
        self._name = name

# Mock Purchase
class Purchase:
    def __init__(self, id_purchase):
        self.id_purchase = id_purchase
        self.finalized = False
    def finalize_purchase(self):
        self.finalized = True
        print(f"Compra {self.id_purchase} finalizada.")

# Mock Delivery
class Delivery:
    def __init__(self, id_delivery):
        self.id_delivery = id_delivery
        self.started = False
    def start_delivery(self):
        self.started = True
        print(f"Entrega {self.id_delivery} iniciada.")
    def receive_notification(self, msg):
        print(f"Entrega {self.id_delivery} recebeu notificação: {msg}")


# Classe Distributor (sua implementação)
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
        
    def __validate_employee(self, employee):
        return hasattr(employee, "register_entry")
    
    def __validate_client(self, client):
        return hasattr(client, "buy")
    
    def notify(self, entity):
        entity.receive_notification("Informação do Sistema: O Sistema foi atualizado")
        
    def __str__(self):
        return f"Distribuidora {self._name} | Clientes: {len(self._clients)}"


# -------------------------------
# Testando a classe Distributor
# -------------------------------
def testar_distributor():
    dist = Distributor("Distribuidora XPTO")

    # Criando mocks
    cliente = Client("Maria")
    funcionario = Employee("Carlos")
    estoque = Stock("Cimento")
    compra = Purchase(101)
    entrega = Delivery(202)

    # Registrando entidades
    dist.register_client(cliente)
    dist.register_employee(funcionario)
    dist.register_stock(estoque)

    # Processando compra
    dist.process_purchase(compra)

    # Despachando entrega
    dist.dispatch_delivery(entrega)

    # Testando notify (duck typing)
    dist.notify(cliente)
    dist.notify(entrega)

    # Testando métodos privados via name mangling
    print("Validação de funcionário:", dist._Distributor__validate_employee(funcionario))
    print("Validação de cliente:", dist._Distributor__validate_client(cliente))

    # Representação amigável
    print(str(dist))


if __name__ == "__main__":
    testar_distributor()
