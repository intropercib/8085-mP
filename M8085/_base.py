
from abc import ABC, abstractmethod
from typing import Dict, Callable

class Instruction(ABC):
    @abstractmethod
    def get_inst(self) -> Dict[str, Callable]:
        pass
