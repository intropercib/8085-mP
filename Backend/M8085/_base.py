"""Base class for 8085 instruction implementations."""

from abc import ABC, abstractmethod
from typing import Dict, Callable

class Instruction(ABC):
    """Abstract base class that all instruction categories must inherit from.
    
    Provides dictionary-style access to instruction methods via __getitem__.
    Subclasses must implement get_inst() to return their instruction mapping.
    """
    
    def __getitem__(self, key: str) -> Callable | None:
        try:
            return self.get_inst()[key]
        except KeyError:
            return f"Instruction '{key}' not found."

    @abstractmethod
    def get_inst(self) -> Dict[str, Callable]:
        """Return a dict mapping instruction mnemonics to their handler methods."""
        pass
