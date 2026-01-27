from datetime import datetime
from ..abstracts.loyalty_system import LoyaltySystem
from ..mixins.review_mixin import ReviewMixin
from ..abstracts.abstract_client import AbstractClient

class Client(ReviewMixin, AbstractClient, LoyaltySystem): 
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
        self.__loyalty_points = loyalty_points
        self.__purchase_history = []
        self._reviews = []
        
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
        
        #v. bruto
        gross_value = quantity_pallets * unit_value_pallet
       
       #desconto acerca do volume 
        discount_rate = self.volume_discount(quantity_pallets)
        discount_value = gross_value * discount_rate
        
        #v. final c desconto add.
        final_value = gross_value - discount_value

        self.__purchase_history.append({
                "Product": product.name,
                "Quantity": quantity_pallets,
                "Final Value": final_value,
                "Date": datetime.now()
        })
        
        if quantity_pallets > 1:
            self.add_loyalty_points(final_value)
        return final_value
    
    def volume_discount(self, quantity_pallets):
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
    
#adiciona pontos acumulativos de acordo com o valor da conta; neste quesito é creditado pontos uando o cliente faz compras acima de 1 pallet de produtos.
    def add_loyalty_points(self, buy_value):
        points = int(buy_value // 10)
        self.__loyalty_points += points
    
#método de resgate de pontos acumulativos; acima de 0; mostra a quantidade de pontos arrecadados/ou não pelo cliente 
    def claim_points(self):
        if self.__loyalty_points <= 0:
            return "O Cliente não possui pontos para resgatar"
        
        points_redeemed = self.__loyalty_points
        self.__loyalty_points = 0
        
        return f"O cliente arrecadou {points_redeemed} pontos com sucesso!"
    
 #cliente checa se recebe/aplica preco promocional no valor da compra; caso possua desconto ou frete grátis ele é informado automaticamente.
    def check_promotion(self, buy_value):
        discount = 0
        
        if self.__loyalty_points >= 500:
            discount = 0.20  
        elif self.__loyalty_points >= 200:
            discount = 0.10
        
        value_with_discount = buy_value - (buy_value * discount)
        
        return{
            "Desconto Aplicado": f"{int(discount * 100)}%",
            "Valor Final": value_with_discount
        }
        
#mecanização de categoria do cliente; é levado em conta o valor que ele deixa no caixa da distribuidora
# (criado com dicionários)
    def client_category(self):
        
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
             
    def summary_client(self):
        return {
            "Name": self.__name,
            "Tipo de Cliente": self.__client_type,
            "Categoria": self.client_category(),
            "Pontos de Fidelidade": self.__loyalty_points,
            "Total de Compras" : self.__purchase_history
        }
        
#verifica se o clinete está ativoo conforme a data presebte na lista de compras:
    def client_status(self):
        
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
        
        :param rating: Nota de 1 a 5 (satisfação do cliente).
        :param comment: Comentário opcional sobre o serviço.
        :return: Mensagem de confirmação.
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
