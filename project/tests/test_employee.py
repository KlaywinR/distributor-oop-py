from datetime import datetime
from models.employee import Employee


# Mock de AbstractEmployee e ClockMixin
class AbstractEmployee:
    pass

class ClockMixin:
    def clock_in(self):
        self._entry_time = datetime.now()
        return f"Entrada registrada às {self._entry_time}"

    def clock_out(self):
        if not self._entry_time:
            return "Funcionário não registrou entrada."
        worked_time = datetime.now() - self._entry_time
        return f"Saída registrada. Tempo trabalhado: {worked_time}"

# Importando a classe Employee (sua implementação)
# Aqui assumimos que ela já está definida no mesmo arquivo ou importada corretamente.

def testar_employee():
    # Criando funcionário
    funcionario = Employee(
        name="Carlos Silva",
        shift="Manhã",
        cpf="123.456.789-00",
        salary=4000,
        id_employee=101,
        departament="Estoque",
        status_employee="Ativo",
        admission_date=datetime(2022, 5, 10),
        contract_type="CLT",
        position="Auxiliar",
        meta_monthly=50,
        overtime=0,
        hours_worked=10  # simulando 10 horas trabalhadas
    )

    print("=== Teste Inicial ===")
    print("Nome:", funcionario.name)
    print("Salário:", funcionario.salary)
    print("Meta Mensal:", funcionario.meta_monthly)
    print("Status:", funcionario.status_employee())

    # Testando revisão de estoque
    estoque = [
        {"product": "Cimento", "pallet_quantity": 20, "storage_type": "Coberto", "condition": "Bom"},
        {"product": "Tijolos", "pallet_quantity": 15, "storage_type": "Aberto", "condition": "Regular"}
    ]
    print("Revisão de Estoque:", funcionario.review_stock(estoque))

    # Testando cálculo de hora extra
    print("Hora extra (dia normal):", funcionario.calculate_overtime("Normal"))
    print("Hora extra (feriado):", funcionario.calculate_overtime("Feriado"))

    # Testando solicitação de férias
    print("Solicitação de Férias:", funcionario.request_vacation())

    # Testando pedido de aumento
    print("Pedido de aumento 10%:", funcionario.request_raise(10))
    print("Pedido de aumento 20%:", funcionario.request_raise(20))

    # Testando ponto eletrônico
    print(funcionario.register_entry())
    print(funcionario.register_exit())

if __name__ == "__main__":
    testar_employee()
