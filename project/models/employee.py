
from datetime import datetime
from ..abstracts.abstract_employee import AbstractEmployee
from ..mixins.clock_mixin import ClockMixin

class Employee(ClockMixin, AbstractEmployee):
    def __init__(self, name, shift, cpf, salary, id_employee, departament, status_employee, admission_date, contract_type, position, meta_monthly, overtime, hours_worked):
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
        return self.__name 
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Nome Inválido")
        self.__name = value

    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salário Inválido")
        self.__salary = value
  
    
    @property
    def meta_monthly(self):
        return self.__meta_monthly

    def status_employee(self):
        return self.__status_employee
    
    def review_stock(self, stock: list[dict]) -> list[dict]:

        reviewed_stock  = []
        
        for item in stock:
            reviewed_stock.append({
                "product": item["product"],
                "pallet_quantity": item["pallet_quantity"],
                "storage_type": item["storage_type"],
                "condition": item["condition"]
            })
                    
        return reviewed_stock
               
#calculo da hora extra com base no tipo de dia trabalhado - normal, domingo o feriado:
#é considerado aspenas as horas que passam da jornada de 8 horas e aplica o adicional de 50 ou 100

    def calculate_overtime(self, day_type = "Normal"):
        standard_daily_hours = 8 #jor. padrao
        
        if self.__hours_worked <= standard_daily_hours:
            return 0.0
    
        extra_hours = self.__hours_worked - standard_daily_hours
        hourly_value = self.__salary / 200
        
        overtime_rate = 2.0  if day_type.lower() in ("Feriado", "Domingo") else 1.5 
            
        overtime_value = extra_hours * hourly_value * overtime_rate
        return round(overtime_value, 2)
            
#? deve ter um método do GERENTE p aprovar as ferias:

    def request_vacation(self):
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
    
    #regra: acima de 15% precisa de aprovaçãoo do gerente:
        if percentage > 15:
            request_raise["Observação"] = "Aumentos acima de 15% necessitam da análise da Gerência"
        return {
            "mensagem": "Olá, o seu pedido de aumento salarial foi registrada com sucesso!",
            "despacho": "O pedido se encontra na análise do Gerente",
            "detalhes": request_raise
        }