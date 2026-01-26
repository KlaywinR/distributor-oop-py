from datetime import date, timedelta
from models.driver import Driver

# Mock de AvailabilityMixin
class AvailabilityMixin:
    def set_availability(self, available: bool):
        self._status = "ATIVO" if available else "INDISPONÍVEL"

# Mock de AbstractDriver
class AbstractDriver:
    pass

# Mock de Delivery
class Delivery:
    def __init__(self, id_delivery):
        self.id_delivery = id_delivery
        self.started = False
        self.completed = False
    
    def start_delivery(self):
        self.started = True
        print(f"Entrega {self.id_delivery} iniciada.")
    
    def complete(self):
        self.completed = True
        print(f"Entrega {self.id_delivery} concluída.")

# Importando a classe Driver (sua implementação)
# Aqui assumimos que ela já está definida no mesmo arquivo ou importada corretamente.

def testar_driver():
    # Criando motorista com CNH válida
    motorista = Driver(
        id_driver=1,
        name="João da Silva",
        cpf="123.456.789-00",
        cnh_category="D",
        cnh_expiration=date.today() + timedelta(days=365),  # CNH válida por 1 ano
        max_capacity_pallets=50,
        region="Nordeste"
    )

    print("=== Teste Inicial ===")
    print(motorista)
    print("CNH válida?", motorista.cnh_is_valid())
    print("Pode operar?", motorista.can_operate())

    # Criando entregas
    entrega1 = Delivery(101)
    entrega2 = Delivery(102)

    # Atribuindo entrega
    motorista.assign_delivery(entrega1)
    motorista.assign_delivery(entrega2)
    print("Entregas atribuídas:", len(motorista))

    # Aceitando e completando entrega
    motorista.accept_delivery(entrega1)
    motorista.complete_delivery(entrega1)

    # Rejeitando entrega
    motorista.reject_delivery()
    print("Status após rejeição:", motorista.status)

    # Registrando várias ocorrências para bloquear motorista
    for i in range(5):
        motorista.register_occurance(f"Infração {i+1}")
    print("Status após infrações:", motorista.status)

    # Representação amigável
    print(str(motorista))


if __name__ == "__main__":
    testar_driver()
