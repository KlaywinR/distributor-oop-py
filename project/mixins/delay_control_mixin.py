
from datetime import datetime

class DelayControlMixin:
    
    def is_delayed(self) -> bool:
        if not  self._finished_at:
            return False
        if not hasattr(self, "_estimated_time"):
            return False
        return datetime.now() > self._estimated_time