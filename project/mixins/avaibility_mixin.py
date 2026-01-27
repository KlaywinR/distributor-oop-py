
class AvailabilityMixin:
    """
     Mixin responsável por verificar a disponibilidade de operação.
    """
    def is_available(self)-> bool:
        """
        Verifica se o objeto está disponível para operar.
        True se estiver ativo e apto a operar, False caso contrário.
        """
        return self._status == "ATIVO" and self.can_operate()