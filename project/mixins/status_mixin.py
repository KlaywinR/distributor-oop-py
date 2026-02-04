class StatusMixin:
    """
    Permite controlar o status do pallet, ativar, bloquear, e verificar o estado atual.
    """
    def block(self):
        """
        Bloqueia o pallet -- muda o status do mesmo.
        """
        self._status = "Bloqueado"
        
    def activate(self):
        """
        Ativa o pallet -- muda o status do mesmo
        """
        self._status = "Ativo"
        
    def is_active(self)-> bool:
        """
        Vê se o pallet está ativo, caso contrário é FALSE.
        """
        return self._status == "Ativo"