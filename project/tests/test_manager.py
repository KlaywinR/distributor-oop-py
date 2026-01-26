# Mock de AuthorizationMixin
class AuthorizationMixin:
    def _authorize(self, message: str):
        print(f"[AUTORIZAÇÃO]: {message}")

# Mock de AbstractManager
class AbstractManager:
    pass

# Mock de Purchase
class Purchase:
    def __init__(self, total_value):
        self.total_value = total_value
        self.approved = False
    
    def mark_as_approved(self):
        self.approved = True
        print("Compra aprovada com sucesso!")

# Mock de Client
class Client:
    def __init__(self, name):
        self.name = name
        self.discount_applied = 0
    
    def apply_discount(self, percentage):
        self.discount_applied = percentage
        print(f"Desconto de {percentage}% aplicado ao cliente {self.name}")

# Mock de Distributor
class Distributor:
    def __init__(self, revenue, clients):
        self._revenue = revenue
        self._clients = clients
    
    def total_revenue(self):
        return self._revenue
    
    def active_clients(self):
        return self._clients

# Mock de Employee
class Employee:
    def __init__(self, name):
        self.name = name
        self.promoted = False
        self.dismissed = False
    
    def promote(self):
        self.promoted = True
        print(f"Funcionário {self.name} promovido!")
    
    def dismiss(self):
        self.dismissed = True
        print(f"Funcionário {self.name} demitido!")

# Classe Manager (sua implementação)
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
        if action == "PROMOTE" and hasattr(employee, "promote"):
            employee.promote()
        elif action == "DISMISS" and hasattr(employee, "dismiss"):
            employee.dismiss()


# -------------------------------
# Testando a classe Manager
# -------------------------------
def testar_manager():
    gerente = Manager()

    # Testando aprovação de compra
    compra1 = Purchase(60000)
    gerente.approve_purchase(compra1)
    print("Compra aprovada?", compra1.approved)

    # Testando desconto
    cliente = Client("Empresa XPTO")
    gerente.approve_discount(cliente, 10)
    print("Desconto aplicado:", cliente.discount_applied)

    # Testando relatório
    distribuidor = Distributor(1000000, ["Cliente A", "Cliente B", "Cliente C"])
    relatorio = gerente.request_report(distribuidor)
    print("Relatório:", relatorio)

    # Testando gestão de funcionário
    funcionario = Employee("Carlos")
    gerente.manage_employee(funcionario, "PROMOTE")
    gerente.manage_employee(funcionario, "DISMISS")
    print("Promovido?", funcionario.promoted)
    print("Demitido?", funcionario.dismissed)


if __name__ == "__main__":
    testar_manager()
