from app.agent.react_agent import ReActAgent
from app.schemas.agent import AgentRequest, AgentResponse
from app.tools.registry import ToolRegistry


class AgentOrchestrator:
    """Manages agent lifecycle and tool registration.

    Responsibilities:
    - Register available tools
    - Create agent instances
    - Handle run lifecycle (init, execute, cleanup)
    - Manage conversation state (TODO)
    """

    def __init__(self):
        self.tool_registry = ToolRegistry()
        self._agent: ReActAgent | None = None
        self._register_default_tools()

    def _register_default_tools(self):
        """Register the built-in tools."""
        from app.tools.calculator import CalculatorTool
        from app.tools.database import DatabaseLookupTool
        from app.tools.search import SearchTool

        self.tool_registry.register(CalculatorTool())
        self.tool_registry.register(SearchTool())
        self.tool_registry.register(DatabaseLookupTool())

    def get_agent(self) -> ReActAgent:
        """Get or create the agent instance."""
        if self._agent is None:
            self._agent = ReActAgent(tool_registry=self.tool_registry)
        return self._agent

    async def run(self, request: AgentRequest) -> AgentResponse:
        """Run the agent on a request."""
        agent = self.get_agent()
        return await agent.run(request)

    def list_tools(self) -> list[dict]:
        """List all registered tools."""
        return self.tool_registry.list_tools()
