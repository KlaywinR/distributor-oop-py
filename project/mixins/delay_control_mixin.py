from datetime import datetime

class DelayControlMixin:
    """
    Responsável por verificar atraso em processos ou entregas.Onde compara o horario atual com o estimado.
    """
    def is_delayed(self) -> bool:
        """
        Verifica se a operação foi concluída com atraso.
        """
        if not  self._finished_at:
            return False
        if not hasattr(self, "_estimated_time"):
            return False
        return datetime.now() > self._estimated_time