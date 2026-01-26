
from datetime import datetime

class MixinPurchase:
    def register_log(self, message: str):
        if not hasattr(self, "_logs"):
            self._logs = []
        self._logs.append(f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] {message}")