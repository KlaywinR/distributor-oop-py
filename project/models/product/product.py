
from project.abstracts.promocional import Promocional
from project.models.product.product_status import ProductStatus
from datetime import date
from typing import Optional
from project.abstracts.promocional import Promocional

class Product(Promocional):
    """
    Representa um produto dentro do sistema de gestão comercial e logística.
        -H: Promocional: fornece regras relacionadas a promoções de preço.
    """
    def __init__(self, name, category,unit_measure,brand,
                 wheight_per_unit,pallets_quantity,barcode,
                 total_units,cost_price, quantity, supplier, 
                 min_stock,origin,units_per_pallet, min_pallets, 
                 unit_price, expiration_date = date , 
                 dimensions= tuple[float, float, float], 
                 status: ProductStatus = ProductStatus.ACTIVE):
        """
        Inicia um produto com dados comerciais e logisticos
        """
        self._name = name 
        self._category = category
        self._brand = brand
        self._barcode = barcode
        self._supplier = supplier
        self._quantity = quantity
        self._origin = origin
        self._expiration_date = expiration_date
        self._dimensions = dimensions
        self._min_stock = min_stock
        self._total_units = total_units
        self._wheight_per_unit = wheight_per_unit
        self._status = status
        self._units_per_pallet = units_per_pallet 
        self._min_pallets = min_pallets
        self._pallets_quantity = pallets_quantity
        self._cost_price = cost_price
        self._unit_measure = unit_measure
        self._unit_price = unit_price
        self._promotion_price: Optional[float] = None
        
    @property
    def barcode(self):
        """""
        Retorna o código de barras.
        """
        return self._barcode
    
    @property
    def units_per_pallet(self):
        """""
        Retorna as unidades por pallet.
        """
        return self._units_per_pallet
    
    @property
    def name(self):
        """""
        Retorna o nome do produto.
        """
        return self._name 
        
    def available_pallets(self):
        """
        Retorna a quantidade de pallets disponíveis em estoque.
        """
        return self._pallets_quantity
    
    def promotion_price(self) ->  Optional[float]:
        """
        Retorna o preço promocional do produto, se existir.
        """
        return self._promotion_price
    
    def total_units_stock(self) -> int:
        """
        Calcula o total de unidades disponíveis em estoque.
        """
        total = self._pallets_quantity * self._units_per_pallet
        print(f"Informação: total de unidades no estoque: {total}")
        return total
    
    def total_stock_value(self) -> float:
        """
        Calcula o valor total do estoque do produto.
        """
        total = self.current_price() * self.total_units_stock()
        print(f"Informação: Valor total do estoque: {total:.2f}")
        return total
    
    def total_weight(self) -> float:
        """ 
        Calcula o peso total do estoque do produto.
          - O cálculo é feito multiplicando o total de unidades
            pelo peso unitário.
        """
        total = self.total_units_stock() * self._wheight_per_unit
        print(f"Informação: Peso total do estoque: {total:.2f} {self._unit_measure}")
        return total
    
    def add_pallets(self, pallets: int) -> None:
        """
         Adiciona pallets ao estoque do produto.
            - O produto estiver ativo;
            - A quantidade informada for maior que zero.
        """
        if self._status != ProductStatus.ACTIVE:
            raise PermissionError(
                "Mensagem de Erro: O produto não está ativo."
            )
        if pallets <= 0:
            raise ValueError(
                "Mensagem de Erro: A quantidade de pallets deve ser positiva."
            )
        self._pallets_quantity += pallets
        
        print (
            f"Estoque em: +{pallets} pallets adicionados | "
            f"Pallets Atuais: {self._pallets_quantity}"
        )
        
    def reserve_pallets(self, quantity: int):
        """
          Reserva pallets do estoque do produto.
            - A reserva diminui temporariamente a quantidade
            disponível em estoque.

        """
        if quantity > self._pallets_quantity:
            raise ValueError("Estoque insuficiente")
        self._pallets_quantity -= quantity

    def remove_pallets(self, pallets: int) -> None:
        """
        Remove uma quantidade de pallets do estoque do produto.
            - A quantidade informada for maior que zero;
            - Houver pallets suficientes em estoque;
            - O produto não estiver vencido.
        """
        if pallets <= 0:
            raise ValueError("Mensagem de Erro: Quantidade Inválida")
        if pallets > self._pallets_quantity:
            raise ValueError("Mensagem de Erro: Estoque insuficiente de pallets para esta operação.")  
        if self.is_expired():
            raise PermissionError( "Mensagem de Erro: O produto está vencido.")
        
        self._pallets_quantity -= pallets
        
        print (
            f"Saída Registrada: {pallets} pallets removidos!"
            f"Pallets Restantes: {self._pallets_quantity}"
        )
        
    def needs_restock(self) -> bool:
        """
        Verifica se o produto precisa de reposição.
         - bool: True se estiver abaixo do mínimo, False caso contrário.
        """
        needs = self._pallets_quantity <= self._min_pallets
        print(f"Reposição Necessária: {'SIM' if needs else 'NÃO'}")
        return needs
    
    def is_expired(self) -> bool:
        """
        Verifica se o produto está vencido.
            - bool: True se estiver vencido, False caso contrário.
        """
        expired = self._expiration_date < date.today()
        print(f"Status de Validade: {'EXPIRADO' if expired else 'VÁLIDO'}")
        return expired

    def block(self) -> None:
        """
        Bloqueia o produto
        """
        self._status = ProductStatus.BLOCKED
        print("O produto se encontra bloqueado")
        
    def activate(self) -> None:
        """Ativa o produto"""
        self._status = ProductStatus.ACTIVE
        print("O produto se enconta ativo")
        
    def discontinued(self) -> None:
        """Descontinua o produto"""
        self._status = ProductStatus.DISCONTINUED
        print("O produto está descontinuado..")
        
    def is_active(self) -> bool:
        """Verifica se o produto esta ativo"""
        return self._status == ProductStatus.ACTIVE

    def profit_per_unit(self) -> float:
        """Calcula o lucro por unidade do produto"""
        profit = self._unit_price - self._cost_price
        print(f"Informação do Sistema: Lucro por unidade: {profit:.2f}")
        return profit
    
    def profit_per_pallet(self) -> float:
        """Calcula o lucro total por pallet"""
        profit = self.profit_per_unit() * self._units_per_pallet
        print(f"Informação do Sistema: Lucro por pallet: {profit:.2f}")
        return profit
    
    def add_promotion(self, new_price):
        """Aplica um preço promocional ao produto"""
        if new_price <= self._cost_price:
            raise ValueError("Informação do Sistema: O preço promocional está abaixo do custo")
        self._promotion_price = new_price
        print(f"Promoção Aplicada: Novo Preço: R$ {new_price:.2f}")
    
    def remove_promotion(self) -> None:
        """Remove o preço promocional adiconado ao produto"""
        self._promotion_price = None
        print("Informação do Sistema: A promoção foi removida.")
         
    def has_promotion(self) -> bool:
        """Verifica se o produto esta possui promoção"""
        return self._promotion_price is not None
        
    def current_price(self) -> float:
        """Retorna o preço atual do produto"""
        return self._promotion_price if self.has_promotion() else self._unit_price

    def __str__(self) -> str:
        """Retorna uma representação textual do produto."""
        return (
        f"\nInformações Gerais do Produto'\n"
        f"Produto: {self._name}\n"
        f"Categoria: {self._category}\n"
        f"Marca: {self._brand}\n"
        f"Código de Barras: {self._barcode}\n"
        f"Fornecedor: {self._supplier}\n"
        f"Origem: {self._origin}\n"
        f"Status: {self._status.name}\n"
        
        f"\n---- Informações sobre o estoque ----\n"
        f"Pallets em Estoque: {self._pallets_quantity}\n"
        f"Unidades por Pallet: {self._units_per_pallet}\n"
        f"Total de Unidades: {self.total_units_stock()}\n"
        f"Estoque Mínimo (Pallets): {self._min_pallets}\n"
        f"Reposição Necessária: {'SIM' if self.needs_restock() else 'NÃO'}\n"
        
        f"\n--- Informações sobre o preço do produto ----\n"
        f"Preço Unitário: R$ {self._unit_price:.2f}\n"
        f"Preço Atual: R$ {self.current_price():.2f}\n"
        f"Em Promoção: {'SIM' if self.has_promotion() else 'NÃO'}\n"
        f"Lucro por Unidade: R$ {self.profit_per_unit():.2f}\n"
        f"Lucro por Pallet: R$ {self.profit_per_pallet():.2f}\n"
        
        f"\n--- Informações sobre a Validade do Produto ---\n"
        f"Data de Validade: {self._expiration_date}\n"
        f"Produto Vencido: {'SIM' if self.is_expired() else 'NÃO'}\n"
        
        f"\n--- Informações sobre as Dimensões do Produto ---\n"
        f"Dimensões (C x L x A): {self._dimensions}\n"
        f"Peso por Unidade: {self._wheight_per_unit:.2f} {self._unit_measure}\n"
        f"Peso Total em Estoque: {self.total_weight():.2f} {self._unit_measure}\n"
        f"-----------------------------------------------------------\n"
    )