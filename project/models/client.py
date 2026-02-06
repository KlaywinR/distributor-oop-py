from datetime import datetime
from project.abstracts.loyalty_system import LoyaltySystem
from project.mixins.review_mixin import ReviewMixin
from project.abstracts.abstract_client import AbstractClient

class Client(ReviewMixin, AbstractClient, LoyaltySystem): 
    """
        ReviewMixin: fornece funcionalidades de avaliação do serviço.
        AbstractClient: define a interface base de um cliente.
        LoyaltySystem: gerencia regras de acúmulo e resgate de pontos.
    """
    def __init__(self, name, cnpj, id_client, credit_limit, costumer_preferences, client_status, registration_date, address, phone, client_type, loyalty_points=0):
        self.__name = name
        self.__cnpj = cnpj
        self.__id_client = id_client
        self.__credit_limit = credit_limit
        self.__costumer_preferences = costumer_preferences
        self.__client_status = client_status
        self.__registration_date = registration_date
        self.__address = address
        self.__phone = phone
        self.__client_type = client_type
        self.__loyalty_points = 0
        self.__purchase_history = []
        self._reviews = []
        self.produtos = {
            "Cimento": {"preco": 45.00, "promocao": 20.00},
            "Arroz": {"preco": 5.50, "promocao": None},
            "Feijão": {"preco": 7.80, "promocao": 7.50}
        }
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Nome Inválido")
        self.__name = value
    
    @property
    def credit_limit(self):
        return self.__credit_limit
    

    def buy(self, product, quantity_pallets: int, unit_value_pallet: float) -> float:
        """
        Registra uma compra realizada pelo cliente.
        - O valor final considera descontos por volume e
         adiciona pontos de fidelidade quando aplicável.
        """
        
        #v. bruto
        gross_value = quantity_pallets * unit_value_pallet
       
       #desconto acerca do volume 
        discount_rate = self.volume_discount(quantity_pallets)
        discount_value = gross_value * discount_rate
        
        #v. final com desconto adicionado.
        final_value = gross_value - discount_value

        self.__purchase_history.append({
                "Product": product,
                "Quantity": quantity_pallets,
                "Final Value": final_value,
                "Date": datetime.now()
        })
        
        if quantity_pallets > 1:
            self.add_loyalty_points(final_value)
        return final_value
    
    def volume_discount(self, quantity_pallets):
        """
        Calcula o percentual de desconto com base no volume comprado.
        """
        if quantity_pallets >= 75:
            return 0.30
    
        elif quantity_pallets >= 50:
            return 0.25
    
        elif quantity_pallets >= 20:
            return 0.15
        
        elif quantity_pallets >= 10:
            return 0.05
        else: 
            return 0
    
    def add_loyalty_points(self, buy_value):
        """
         Adiciona pontos de fidelidade ao cliente.
        - A cada R$10,00 gastos, 1 ponto é creditado,
        desde que a compra seja superior a 1 pallet.
        """
        if buy_value >0:
            points = int(buy_value // 10)
            self.__loyalty_points += points
            return points
        return 0
    
 
    def claim_points(self):
        """Resgate dos pontos de fidelidade acumulados."""
        points_redeemed = self.__loyalty_points
        self.__loyalty_points = 0
        
        return points_redeemed
    
    
    def check_promotion(self, product_name):
        produto = self.produtos.get(product_name)
        if product_name and produto.get["promocao"] is not None:
            return produto["promocao"]
        return None
        
    def client_category(self):
        """
        Define a categoria comercial do cliente com base
        no faturamento total acumulado.
        """
        DIAMOND = 1000000
        GOLD = 300000
        SILVER = 100000
        
        #calculo do faturamento total
        total_revenue = sum(p["Final Value"] for p in self.__purchase_history)
        
        if total_revenue >= DIAMOND:
            return {
                "Categoria Atual": "Diamante",
                "Nivel Comercial": "Top Account",
                "Descrição da Categoria": "Este cliente possui visão estratégica e altos valores em faturamento",
                "Benefícios": [
                    "Possui desconto exclusivo",
                    "Atendimento prioritário",
                    "Crédito Estendido",
                    "Negociação personalizada com a distribuidora"
                ]
                
            }
        elif total_revenue >= GOLD:
            return {
                "Categoria Atual": "Ouro",
                "Nivel Comercial": "Alta performance",
                "Descrição da Categoria": "Cliente com excelente volume de compras",
                "Benefícios": [
                    "Desconto Diferenciado",
                    "Crédito Facilitado pela distribuidora"
                ]
            }
            
        elif total_revenue >= SILVER:
            return {
                "Categoria Atual": "Prata",
                "Nivel Comercial": "Em crescimento",
                "Descrição da Categoria": "Este cliente possui ótimo potencial de crescimento",
                "Benefícios": [
                    "Programa de fidelidade padrão"
                ]
            }
            
        else:
            return {
                "Categoria Atual": "Bronze",
                "Nivel Comercial": "Ainda iniciando",
                "Descrição da Categoria": "Este cliente está em fase inicial de relacionamento",
                "Benefícios": [
                    "Condições comerciais básicas"
                ]
            }
             
    def client_status(self):
        """
        Verifica o status do cliente no sistema.
            - O cliente é considerado ativo se realizou compras nos ultimos 90 dias.
        """
        if self.__client_status == "BLOQUEADO":
            return "Cliente Inativo no Sistema"
        
        if not self.__purchase_history:
            return "Cliente Ativo no Sistema"
        
        last_purchase_date = self.__purchase_history[-1]["Date"]
        days = (datetime.now() - last_purchase_date).days

        return "Cliente Ativo" if days <= 90 else "Cliente Inativo"


    def evaluate_service(self, rating: int, comment: str = ""):
        """
        Permite que o cliente avalie o serviço da distribuidora.
        """
        if rating < 1 or rating > 5:
            raise ValueError("A nota deve estar entre 1 e 5")
        
        review = {
            "Rating": rating,
            "Comment": comment,
            "Date": datetime.now()
        }
        
        self._reviews.append(review)
        
        return f"Avaliação registrada com sucesso! Nota: {rating}, Comentário: {comment if comment else 'Sem comentário'}"

    def summary_client(self):
        """ Retorna um resumo completo do cliente."""
        return {
            "Name": self.__name,
            "Tipo de Cliente": self.__client_type,
            "Categoria": self.client_category(),
            "Pontos de Fidelidade": self.__loyalty_points,
            "Total de Compras" : self.__purchase_history
        }
        