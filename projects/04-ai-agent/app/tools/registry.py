from app.tools.base import BaseTool


class ToolRegistry:
    """Registry for managing available tools.

    Tools are registered by name and looked up by the agent
    when deciding which tool to use.
    """

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool

    def unregister(self, name: str) -> None:
        """Remove a tool from the registry."""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found")
        del self._tools[name]

    def get(self, name: str) -> BaseTool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        """List all registered tools with metadata."""
        return [tool.to_dict() for tool in self._tools.values()]

    def has(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self._tools
