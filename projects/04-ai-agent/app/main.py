from fastapi import FastAPI

from app.api.routes import agent

app = FastAPI(
    title="AI Agent System",
    description="A ReAct-style AI agent with tool use",
    version="0.1.0",
)

app.include_router(agent.router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
