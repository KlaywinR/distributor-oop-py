

class StatusMixin:
    """
    Serve para controlar o status do pallet.
    """
    
    def block(self):
        self._status = "Bloqueado"
        
    def activate(self):
        self._status = "Ativo"
        
    def is_active(self)-> bool:
        return self._status == "Ativo"