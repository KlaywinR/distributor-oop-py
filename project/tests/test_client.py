from datetime import datetime
from models.client import Client

class Product:
    def __init__(self, name):
        self.name = name

def testar_client():

    cliente = Client(
        name="Empresa XPTO",
        cnpj="12.345.678/0001-99",
        id_client=101,
        credit_limit=50000,
        costumer_preferences=["Cimento", "Tijolos"],
        client_status="BLOQUEADO",
        registration_date=datetime(2024, 5, 10),
        address="Rua das Flores, 123",
        phone="(84) 99999-8888",
        client_type="Distribuidor",
        loyalty_points=0
    )
    
    produto1 = Product("Cimento")
    produto2 = Product("Tijolos")
    valor1 = cliente.buy(produto1, quantity_pallets=15, unit_value_pallet=1000)
    print("Compra 1:", valor1)
    valor2 = cliente.buy(produto2, quantity_pallets=60, unit_value_pallet=800)
    print("Compra 2:", valor2)
    print("Pontos acumulados:", cliente.summary_client()["Pontos de Fidelidade"])
    print(cliente.claim_points())
    print(cliente.check_promotion(20000))
    print(cliente.client_category())
    print(cliente.client_status())
    print(cliente.evaluate_service(5, "Excelente atendimento!"))
    print(cliente.evaluate_service(4))
    print("Resumo do Cliente:")
    print(cliente.summary_client())


if __name__ == "__main__":
    testar_client()
