
class AvailabilityMixin:
    def is_available(self)-> bool:
        return self._status == "ATIVO" and self.can_operate()