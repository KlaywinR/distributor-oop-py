
from datetime import datetime
from ..abstracts.abstract_employee import AbstractEmployee
from ..mixins.clock_mixin import ClockMixin

class Employee(ClockMixin, AbstractEmployee):
    
    def __init__(self, name, shift, cpf, salary, id_employee, departament, status_employee, 
                 admission_date, contract_type, position, meta_monthly, overtime, hours_worked):
        self.__name = name 
        self.__shift = shift
        self.__id_employee = id_employee
        self.__departament = departament
        self.__salary = salary 
        self.__cpf = cpf
        self.__status_employee = status_employee
        self.__admission_date = admission_date
        self.__contract_type = contract_type
        self.__position = position
        self.__meta_monthly = meta_monthly
        self._overtime = overtime
        self.__hours_worked = hours_worked
        self._entry_time = None

    @property
    def name(self):
        """
        Retorna o nome do funcionário.
        """
        return self.__name 
    
    @name.setter
    def name(self, value):
        """Atualiza o nome do funcionário."""
        if not value:
            raise ValueError("Nome Inválido")
        self.__name = value

    @property
    def salary(self):
        """Retorna o salario"""
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        """Muda o valor do salário"""
        if value < 0:
            raise ValueError("Salário Inválido")
        self.__salary = value
  
    
    @property
    def meta_monthly(self):
        """Mostra a mete mensal do funcionario"""
        return self.__meta_monthly

    def status_employee(self):
        """Retorna o status de employee"""
        return self.__status_employee
    
    def review_stock(self, stock: list[dict]) -> list[dict]:
        """
            - Lista de dicionários representando produtos do estoque
            - Lista com informações essenciais do estoque revisado
        """
        reviewed_stock  = []
        
        for item in stock:
            reviewed_stock.append({
                "product": item["product"],
                "pallet_quantity": item["pallet_quantity"],
                "storage_type": item["storage_type"],
                "condition": item["condition"]
            })
                    
        return reviewed_stock

    def calculate_overtime(self, day_type = "Normal"):
        """
        Calcula o valor da hora extra do funcionário.
        Considera apenas as horas trabalhadas acima de 8h diárias.
        Aplica adicional de:
        - 50% em dias normais
        - 100% em domingos ou feriados
        """
        standard_daily_hours = 8 #jor. padrao
        
        if self.__hours_worked <= standard_daily_hours:
            return 0.0
    
        extra_hours = self.__hours_worked - standard_daily_hours
        hourly_value = self.__salary / 200
        
        overtime_rate = 2.0  if day_type.lower() in ("Feriado", "Domingo") else 1.5 
            
        overtime_value = extra_hours * hourly_value * overtime_rate
        return round(overtime_value, 2)
            
    def request_vacation(self):
        """Solicitação de Ferias"""
        if self.__status_employee.lower() == "ferias":
            return "O funcionário se encontra em recesso."
  
        vacation_request = {
            "employee": self.__name,
            "employee_id": self.__id_employee,
            "departament": self.__departament,
            "request_date": datetime.now(),
            "status": "Aguardando a avaliação do Gerente"
        }
        
        return {
            "mensagem": "Olá, a sua solicitação de férias foi registrada com sucesso!",
            "despacho": "O pedido se encontra na análise do Gerente",
            "detalhes": vacation_request
        }

    def request_raise(self, percentage):
        """
        - Percentuais acima de 15% exigem aprovação da gerência.
        """
        if percentage <= 0:
            return "Este percentual de aumento é inválido."
        request_raise = {
            "employee": self.__name,
            "employee_id": self.__id_employee,
            "current_salary": self.__salary,
            "request_percentage": percentage,
            "request_date": datetime.now(),
            "status": "Aguardando a avaliação do Gerente"
        }

        if percentage > 15:
            request_raise["Observação"] = "Aumentos acima de 15% necessitam da análise da Gerência"
        return {
            "mensagem": "Olá, o seu pedido de aumento salarial foi registrada com sucesso!",
            "despacho": "O pedido se encontra na análise do Gerente",
            "detalhes": request_raise
        }