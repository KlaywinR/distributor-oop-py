from datetime import datetime

class AuditMixin:
    """
    Registrar logs de auditoria + Adição do SRP onde encapsula o comportamento da auditoria.  
    """
    def _log(self, message:  str):
        if not hasattr(self, "_audit_logs"):
            self._audit_logs = []
        self._audit_logs.append(
               f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] {message}"
        )
        