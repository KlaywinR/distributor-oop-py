
from ..abstracts.abstract_purchase import AbstractPurchase
from ..mixins.mixin_purchase import MixinPurchase

class Purchase(AbstractPurchase, MixinPurchase):
    """
    - AbstractPurchase para garantir um contrato mínimo de comportamento;
    - MixinPurchase para reutilizar funcionalidades auxiliares (ex: logs)
    - SRP: compra cuida apenas do processo de compra.
    - OCP: promoções e impostos podem ser estendidos.
    - DI: depende de abstrações.
    """
    
    def __init__(self, client, seller, product, quantity_pallets: int, unit_value_pallet: int):
        super().__init__(client, seller, product, quantity_pallets)
        self._logs = []
        self._payment_method = None
        
    @property
    def status(self):
        """Retorna o status atual da compra"""
        return self._status

    @property
    def total_value(self):
        """Retorna o vaçlo total da compra"""
        return self._total_value
    
    def _apply_promotion(self) -> float:
        """Aplica regras de preço promocional ao produto."""
        return self._product.current_price()
    
    def _validate_stock(self):
        """ Valida se há pallets suficientes disponíveis em estoque."""
        avaiLable = self._product.available_pallets()
        if self._quantity_pallets > avaiLable:
            raise ValueError(f"Estoque Insuficiente." f"Disponivel: {avaiLable} pallets ao todo")
                
    def _validate_credit_limit(self):
        """ Verifica se o cliente possui limite de crédito suficiente."""
        total = self.calculate_total()
        if total > self._client.credit_limit:
            raise PermissionError("Limite de crédito do cliente excedido!")
                  
    def calculate_taxes(self, value: float) -> float:
        """ Calcula os impostos sobre o valor informado."""
        tax_rate = 0.12
        return value * tax_rate
    
    def calculate_total(self):
        """
         - Preço unitário com promoção;
         - Desconto por volume;
         - Cálculo de impostos;
         - Registro de log financeiro.

        """
        unit_price = self._apply_promotion()
        
        gross_value = unit_price * self._quantity_pallets
        
        discount_rate = self._client.volume_discount(self._quantity_pallets)
        discount_value = gross_value * discount_rate
    
        subtotal = gross_value - discount_value
        taxes = self.calculate_taxes(subtotal)    
        final_value = subtotal + taxes
        
        self._total_value = final_value
        self.register_log(
            f"Valor Bruto Calculado: {gross_value:.2f}"
            f"Valor com desconto: R$ {discount_rate * 100: .0f}%"
            f"Impostos: {taxes:.2f}" 
            f"Valor final: {final_value: .3f}"
        )
        return final_value
    
    def simulate_purchase(self):
        """ Simula uma compra sem alterar estoque ou status."""
        self._validate_stock()
        unit_price = self._apply_promotion()
        
        gross = unit_price * self._quantity_pallets
        discount = gross * self._client.volume_discount(self._quantity_pallets)
        subtotal = gross - discount
        taxes = self.calculate_taxes(subtotal)
      
        return {
            "valor bruto": gross,
            "desconto": discount,
            "valor_final": subtotal + taxes
        }
       
    def reserve_pallets(self):
        """ Reserva pallets no estoque antes da finalização da compra."""
        self._validate_stock()
        self._product.reserve_pallets(self._quantity_pallets)
        self.register_log("Pallets Reservados")
        
    def set_payment_method(self, method: str):
        """Define o método de pagamento da compra"""
        allowed = ["PIX", "CREDIT", "DEBIT", "BOLETO"]
        if method not in allowed:
            raise ValueError("Método de pagamento inválido")
        self._payment_method = method
        self.register_log(f"Método de pagamento escolhido pelo cliente: {method}")
    
    def finalize_purchase(self):
        """ Finaliza a compra executando todas as validações necessárias."""
        if self.status != "PENDING":
            raise RuntimeError("A compra já foi processada")
        self._validate_stock()
        self.calculate_total()
        self._validate_credit_limit()
        
    #como a compra ja foi atualizada; o estoque atualiza:
        self._product.remove_pallets(self._quantity_pallets)
        
        #o cliente faz a compra
        self._client.buy(
            self._product,
            self._quantity_pallets,
            self._product.current_price()
        )
        #o seller registra a vensa:
        self._seller.make_sale(
            self._client,
            self._product,
            self._quantity_pallets
        )
        self._seller.add_pallets_sold(self._quantity_pallets)
        self._status = "COMPLETED"
        self.register_log("Compra feita com sucesso!")
        
        return self.total_value
    
    def mark_as_approved(self):
        """ Marca a compra como aprovada pela gerência."""
        self._status = "APPROVED"
            
    def cancel_purchase(self):
        """ Cancela a compra, desde que ainda não tenha sido finalizada."""
        if self._status == "COMPLETED":
            raise RuntimeError("Compra ja finalizada, não pode ser cancelada!")
        self._status = "CANCELED"
        self.register_log("Compra Cancelada")
        
    def issue_invoice(self):
        """Emite a nota fiscal da compra finalizada."""
        if self._status != "COMPLETED":
         raise RuntimeError("Compra não finalizada")

        invoice = {
        "cliente": self._client.name,
        "produto": self._product.name,
        "quantidade_pallets": self._quantity_pallets,
        "valor": self._total_value,
        "pagamento": self._payment_method,
        "data": self._date.strftime("%d/%m/%Y")
    }

        self.register_log("Nota fiscal emitida")
        return invoice

    def __str__(self):
        """Representação Textual"""
        return (
            f"Compra do Cliente: {self._client.name}\n"
            f"Produto: {self._product.name}\n"
            f"Quantidade de Pallets: {self._quantity_pallets}\n"
            f"Status: {self.status}\n"
            f"Valor: {self._total_value}\n"
        )
