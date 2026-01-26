  
class ReportMixin:
#! principio SRP   
    def total_revenue(self):
        return sum(p.total_value for p in self._purchases if p.status == "COMPLETED")
    
    def active_clients(self):
        return [c for c in self._clients if c.client_status() == "Cliente Ativo"]