import uuid

from app.agent.base import BaseAgent
from app.core.config import settings
from app.schemas.agent import (
    AgentRequest,
    AgentResponse,
    AgentStep,
    ToolCall,
    ToolResult,
)
from app.tools.registry import ToolRegistry


class ReActAgent(BaseAgent):
    """ReAct (Reason + Act) agent implementation.

    The ReAct loop:
        1. THOUGHT: Reason about the current state
        2. ACTION: Choose and execute a tool
        3. OBSERVATION: Receive the tool's result
        4. Repeat until ready to answer

    Reference: https://arxiv.org/abs/2210.03629
    """

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.max_iterations = settings.MAX_ITERATIONS

    def think(self, request: AgentRequest, history: list[AgentStep]) -> str:
        """Analyze the situation and reason about next steps.

        TODO: Replace mock reasoning with real LLM call:

            messages = [
                {"role": "system", "content": REACT_SYSTEM_PROMPT},
                {"role": "user", "content": request.query},
            ]
            # Add history as assistant/user messages
            for step in history:
                if step.thought:
                    messages.append({"role": "assistant", "content": f"Thought: {step.thought}"})
                if step.observation:
                    messages.append({"role": "user", "content": f"Observation: {step.observation.result}"})

            response = llm.chat(messages)
            return response.content
        """
        # Mock reasoning for testing
        step_num = len(history) + 1
        tools = self.tool_registry.list_tools()

        if step_num == 1:
            return (
                f"I need to answer: '{request.query}'. "
                f"Available tools: {[t['name'] for t in tools]}. "
                f"Let me think about which tool to use."
            )
        elif step_num <= 3:
            return f"Continuing to work on the problem. Step {step_num}."
        else:
            return "I have enough information to provide an answer."

    def decide(self, thought: str, available_tools: list[dict]) -> ToolCall | str:
        """Decide whether to use a tool or give a final answer.

        TODO: Replace with real LLM output parsing:

            response = llm.chat(messages)
            # Parse response for tool calls
            # If response contains "Final Answer:", return the answer string
            # If response contains "Action:", parse and return ToolCall
        """
        # Mock decision logic: use calculator if query looks like math
        if any(
            op in thought.lower()
            for op in ["calculate", "compute", "math", "+", "-", "*", "/"]
        ):
            return ToolCall(
                tool_name="calculator",
                arguments={"expression": "2 + 2"},
                call_id=str(uuid.uuid4()),
            )

        # If we've been going for a while, give a final answer
        if "enough information" in thought or "answer" in thought.lower():
            return "Based on my analysis, here is the answer to your question."

        # Otherwise, mock a tool call
        if available_tools:
            tool = available_tools[0]
            return ToolCall(
                tool_name=tool["name"],
                arguments={},
                call_id=str(uuid.uuid4()),
            )

        return "I don't have the right tools to answer this question."

    def act(self, decision: ToolCall | str) -> ToolResult | None:
        """Execute a tool call."""
        if isinstance(decision, str):
            return None

        tool = self.tool_registry.get(decision.tool_name)
        if tool is None:
            return ToolResult(
                tool_name=decision.tool_name,
                call_id=decision.call_id,
                error=f"Tool '{decision.tool_name}' not found",
                success=False,
            )

        try:
            result = tool.execute(**decision.arguments)
            return ToolResult(
                tool_name=decision.tool_name,
                call_id=decision.call_id,
                result=result,
                success=True,
            )
        except Exception as e:
            return ToolResult(
                tool_name=decision.tool_name,
                call_id=decision.call_id,
                error=str(e),
                success=False,
            )

    def respond(self, request: AgentRequest, history: list[AgentStep]) -> AgentResponse:
        """Build the final response."""
        tool_calls = sum(1 for s in history if s.action is not None)

        # Extract final answer from last step
        answer = "I was unable to determine an answer."
        if history:
            last = history[-1]
            if last.observation and last.observation.success:
                answer = f"Result: {last.observation.result}"
            elif last.thought:
                answer = last.thought

        return AgentResponse(
            answer=answer,
            steps=history,
            tool_calls_made=tool_calls,
            iterations=len(history),
        )

    async def run(self, request: AgentRequest) -> AgentResponse:
        """Execute the full ReAct loop."""
        history: list[AgentStep] = []
        max_iter = min(request.max_iterations, self.max_iterations)

        for i in range(max_iter):
            step = AgentStep(step_number=i + 1)

            # Think
            step.thought = self.think(request, history)

            # Decide
            available_tools = self.tool_registry.list_tools()
            decision = self.decide(step.thought, available_tools)

            # If final answer, we're done
            if isinstance(decision, str):
                step.observation = ToolResult(
                    tool_name="final_answer",
                    result=decision,
                    success=True,
                )
                history.append(step)
                break

            # Act
            step.action = decision
            step.observation = self.act(decision)
            history.append(step)

            # If tool call failed, note it and continue
            if step.observation and not step.observation.success:
                continue

        return self.respond(request, history)
