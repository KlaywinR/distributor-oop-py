
from project.models.employee import Employee
from abc import abstractmethod, ABC
from project.mixins.seller_mixin import ReportMixin
from project.abstracts.abstract_seller import AbstractSeller
from project.interfaces.seller_interface import CustomerServiceInterface

    
class Seller(Employee, AbstractSeller,CustomerServiceInterface, ReportMixin): 
    def __init__(self, name, shift, cpf, salary,id_employee,departament,
                 status_employee,admission_date,contract_type,
                 position,meta_monthly, overtime, hours_worked, commision_percentual):
        
        super().__init__(name, shift, cpf, salary, id_employee,
                         departament, status_employee, admission_date,
                         contract_type, position, meta_monthly, overtime, 
                         hours_worked)
        
        self.__costumers_served = []
        self.__pallets_sold = 0
        self.__quantity_invites = []
        self.__comission_percentual = commision_percentual
        self.__sales_made = []
        
    @property
    def meta_monthly(self):
        return super().meta_monthly
    
    @meta_monthly.setter
    def meta_monthly(self, value):
        if value <= 0:
            raise ValueError("A meta deve ser maior do que zero")
        self._Employee__meta_monthly = value
        
    @property
    def pallets_sold(self):
        return self.__pallets_sold
        
    def attend_costumer(self, customer):
        self.__costumers_served.append(customer)
        
    def make_sale(self, costumer, product, quantity):
        sale = {
            "costumer":costumer,
            "product":product,
            "quantity":quantity
        }
        self.__sales_made.append(sale)
        
    def calculate_comissions(self):
        return self.__pallets_sold * self.__comission_percentual
    
    def respond_to_complaint(self, client):
        return f"Reclamação do cliente {client} foi respondida"

    def add_pallets_sold(self, quantity):
        if quantity <= 0:
            raise ValueError("A quantidade é inválida")
        self.__pallets_sold += quantity

    def see_costumer_credit(self, client):
            if hasattr(client, "credit_score"):
                if client.credit_score >= 600:
                    return f"O cliente {client.name} possui crédito aprovado!"
                else:
                    return f"O cliente {client.name} não possui crédito aprovado!"
            else:
                return "O cliente não possui o atributo de 'credit_score'"
            
    def follow_costumer(self, client):
        return f"Acompanhamento realizado com o cliente {client}"
    
    def apply_costumer_benefi(self, client):
        return f"O benefício de fidelidade foi aplicado ao cliente {client}"
    
    def negotiate_price(self, discount):
        if discount < 0 or discount > 0.15:
            raise ValueError("O desconto deve encontrar-se entre 0% e 15%")
        return f"Desconto de {discount * 100:.0f}% aprovado!"
    
    def verify_meta_monthly(self):
        return self.meta_monthly <= self.__pallets_sold          

    def register_service(self, client):
        self.__quantity_invites.append(client)
        
    def request_evaluation(self, note):
        if note < 1 or note > 5:
            raise ValueError(" A nota se encontra em uma escala de 1 a 5.")
    
    def sumary_sales(self):
        """
        Função: Retornar um sumário de vendas com o número de clientes atendidos,
                número de vendas realizadas, pallets vendidos e o calcular a comissão
                acerca das ações do funcionário.
        """
        return {
        "clientes_atendidos": len(self.__costumers_served),
        "vendas_realizadas": len(self.__sales_made),
        "paletes_vendidos": self.__pallets_sold,
        "comissao": self.calculate_comissions()
    }
   
    def __str__(self): return f"Seller {self._Employee__name} - Vendas: {len(self.__sales_made)}"
    
    def __iter__(self): return iter(self.__sales_made)
  
    def __len__(self): return len(self.__sales_made)
    