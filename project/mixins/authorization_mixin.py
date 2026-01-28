
class AuthorizationMixin:
    """
    Usado para realizar autorizações do sistema.
    """
    def _authorize(self, reason: str):
        """
        Uma ação exibindo o motivo da autorização.
        """
        print(f"[AUTORIZADO] {reason}")