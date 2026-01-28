
from datetime import datetime

class MovementMixin:
    """
    Responsável por registrar historico de movimentações.
    """
    def register_movement(self, description: str):
        """
        Registra uma movimentação no histórico.
        """
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        if not hasattr(self, "_movement_history"):
            self._movement_history.append(f"[{data}] {description}")