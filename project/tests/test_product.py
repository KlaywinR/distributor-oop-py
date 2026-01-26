from datetime import date, timedelta
from enum import Enum
from products.product import Product
from products.product_status import ProductStatus


# Mock de Promocional (classe base)
class Promocional:
    pass

# Importando a classe Product (a sua implementação)
# Aqui assumimos que ela já está definida no mesmo arquivo ou importada corretamente.

def testar_product():
    # Criando produto válido
    produto = Product(
        name="Cimento CP-II",
        category="Construção",
        unit_measure="kg",
        brand="Votorantim",
        wheight_per_unit=50,          # cada unidade pesa 50kg
        pallets_quantity=20,          # estoque inicial: 20 pallets
        barcode="1234567890123",
        total_units=0,
        cost_price=25.00,
        quantity=1000,
        supplier="Fornecedor ABC",
        min_stock=200,
        origin="Brasil",
        units_per_pallet=40,          # cada pallet tem 40 unidades
        min_pallets=5,
        unit_price=40.00,
        expiration_date=date.today() + timedelta(days=180),  # vence em 6 meses
        dimensions=(1.2, 0.8, 1.5),
        status=ProductStatus.ACTIVE
    )

    print("=== Teste Inicial ===")
    print(produto)

    # Testando cálculo de estoque
    produto.total_units_stock()
    produto.total_stock_value()
    produto.total_weight()

    # Adicionando pallets
    produto.add_pallets(5)

    # Reservando pallets
    produto.reserve_pallets(3)

    # Removendo pallets
    produto.remove_pallets(2)

    # Testando reposição
    produto.needs_restock()

    # Testando validade
    produto.is_expired()

    # Bloqueando e reativando produto
    produto.block()
    produto.activate()

    # Descontinuando produto
    produto.discontinued()

    # Testando lucro
    produto.profit_per_unit()
    produto.profit_per_pallet()

    # Aplicando promoção
    produto.add_promotion(35.00)
    print("Preço atual com promoção:", produto.current_price())

    # Removendo promoção
    produto.remove_promotion()
    print("Preço atual sem promoção:", produto.current_price())

    print("=== Teste Final ===")
    print(produto)


if __name__ == "__main__":
    testar_product()
