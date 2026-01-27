
from ..interfaces.interface_manager import InterfaceManager
from abc import ABC

class AbstractManager(InterfaceManager, ABC):
    def __init__(self, name, registration):
        self._name = name 
        self._registration = registration
