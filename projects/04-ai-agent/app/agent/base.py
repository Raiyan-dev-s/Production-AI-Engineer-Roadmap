from abc import ABC, abstractmethod
from typing import Any

from app.schemas.agent import AgentRequest, AgentResponse


class BaseAgent(ABC):
    """Abstract base class for all agents.

    Every agent implements the core loop:
        think -> decide -> act -> respond
    """

    @abstractmethod
    def think(self, request: AgentRequest, history: list) -> str:
        """Analyze the current state and reason about what to do next.

        Args:
            request: The original user request.
            history: Previous steps in the current run.

        Returns:
            A thought/reasoning string.
        """
        ...

    @abstractmethod
    def decide(self, thought: str, available_tools: list) -> Any:
        """Decide whether to use a tool or provide a final answer.

        Returns:
            - A dict with tool_name and arguments if a tool should be used.
            - A string if this is the final answer.
        """
        ...

    @abstractmethod
    def act(self, decision: Any) -> Any:
        """Execute a tool call based on the decision.

        Args:
            decision: Dict containing tool_name and arguments.

        Returns:
            The tool's result.
        """
        ...

    @abstractmethod
    def respond(self, request: AgentRequest, history: list) -> AgentResponse:
        """Build the final response from the accumulated history."""
        ...

    @abstractmethod
    async def run(self, request: AgentRequest) -> AgentResponse:
        """Execute the full agent loop."""
        ...
