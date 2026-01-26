
from datetime import datetime

class ClockMixin:
    """
    O Mixin acima encapsula o controle de ponto, onde permite o reuso em diferentes tipos de funcionários.
    O mesmo não é acoplado ao modelo final da classe.
    """
    
    def register_entry(self):
        if getattr(self,"_entry_time", None) is not None:
            return "Sua entrada já foi registrada..."
        self._entry_time = datetime.now()
        return "A entrada foi regiistrada com sucesso!."
    
    
    def register_exit(self):
        if getattr(self,"_entry_time", None):
            return "A entrada não foi registrada"
        
        #guarda o horario atual como o de saida
        exit_time = datetime.now()
        worked_hours = (exit_time - self._entry_time).total_seconds() / 3600
        
        self._hours_worked += worked_hours
        if worked_hours > 8:
            self._overtime += worked_hours - 8
            
        self._entry_time = None
        return "A Saída foi registrada"   