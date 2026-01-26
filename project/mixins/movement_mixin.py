
from datetime import datetime

class MovementMixin:
    def register_movement(self, description: str):
        data = datetime.now().strftime("%d/%m/%Y %H: %M")
        if not hasattr(self, "_movement_history"):
            self._movement_history.append(f"[{data}] {description}")