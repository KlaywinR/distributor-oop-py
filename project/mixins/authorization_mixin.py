
class AuthorizationMixin:
    def _authorize(self, reason: str):
        print(f"[AUTORIZADO] {reason}")