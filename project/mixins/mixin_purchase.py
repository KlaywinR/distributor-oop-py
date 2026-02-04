from datetime import datetime

class MixinPurchase:
    """
    Registra logs relacionados a compras. Onde centrailiza o controle de eventos e ações
    """

    def register_log(self, message: str):
        """
        Registra uma mensage log com data e hora.
        """
        if not hasattr(self, "_logs"):
            self._logs = []
        self._logs.append(f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] {message}")