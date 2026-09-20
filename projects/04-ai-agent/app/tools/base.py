from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Abstract base class for all tools.

    Every tool must define:
    - name: unique identifier
    - description: what the tool does (used by the agent to decide when to use it)
    - execute: the actual implementation
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name (e.g., 'calculator', 'search')."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what the tool does.

        This is critical — the agent uses this to decide which tool to use.
        Make it clear and specific.
        """
        ...

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool with the given arguments.

        Returns:
            The tool's result (any JSON-serializable type).
        """
        ...

    def to_dict(self) -> dict:
        """Serialize tool metadata for API responses."""
        return {
            "name": self.name,
            "description": self.description,
        }
