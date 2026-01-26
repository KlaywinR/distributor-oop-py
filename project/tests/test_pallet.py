# Mock de AbstractPallet

from models.pallet  import Pallet


class AbstractPallet:
    def __init__(self, id_pallet, product, max_capacity, max_wheight):
        self._id_pallet = id_pallet
        self._product = product
        self._max_capacity = max_capacity
        self._max_wheight = max_wheight
        self._quantity_products = 0
        self._current_weight = 0.0

# Mock de StatusMixin
class StatusMixin:
    def change_status(self, new_status):
        self._status = new_status

# Mock de Produto
class Product:
    def __init__(self, name, wheight_per_unit):
        self.name = name
        self._wheight_per_unit = wheight_per_unit

    def __str__(self):
        return f"{self.name} ({self._wheight_per_unit}kg/unidade)"


# Testando a classe Pallet
def testar_pallet():
    produto = Product("Cimento", 50)  # cada unidade pesa 50kg
    pallet = Pallet(id_pallet=1, product=produto, max_capacity=100, max_wheight=5000, location_in_stock="A1")

    print("Status inicial:", pallet.status)
    print("Localização:", pallet.location_in_stock)

    # Adicionando produtos
    pallet.add_products(50)
    print("Quantidade após adicionar:", pallet.quantity_products)
    print("Peso atual:", pallet.current_wheight)

    # Removendo produtos
    pallet.remove_products(20)
    print("Quantidade após remover:", pallet.quantity_products)
    print("Peso atual:", pallet.current_wheight)

    # Testando limites
    print("Está vazio?", pallet.is_empty())
    print("Está cheio?", pallet.is_full())

    # Alterando status
    pallet.status = "Bloqueado"
    print("Novo status:", pallet.status)

    # Representação amigável
    print(str(pallet))


if __name__ == "__main__":
    testar_pallet()
