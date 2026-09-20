from fastapi import APIRouter, HTTPException

from app.agent.orchestrator import AgentOrchestrator
from app.schemas.agent import AgentRequest, AgentResponse

router = APIRouter()

# Shared orchestrator (in production, use dependency injection)
_orchestrator = AgentOrchestrator()


@router.post("/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Run the agent on a query.

    The agent will:
    1. Think about the problem
    2. Decide which tools to use
    3. Execute tools and observe results
    4. Repeat until it can answer
    """
    try:
        response = await _orchestrator.run(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent failed: {e!s}") from e


@router.get("/agent/tools")
async def list_tools():
    """List all available tools."""
    return {"tools": _orchestrator.list_tools()}
