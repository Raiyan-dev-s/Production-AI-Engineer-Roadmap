# AI Agents

## What to Learn

Building autonomous systems that use LLMs to reason, plan, and act — moving beyond simple prompt/response to goal-driven behavior.

## Why It Matters

Agents are the bridge between "AI that answers questions" and "AI that does work." They enable complex workflows: research, data collection, code generation, multi-step reasoning.

## Concepts Checklist

- [ ] **Agent Loop**: perceive → think → act → observe → repeat
- [ ] **Tool Use**: defining tools, passing tools to LLMs, handling tool results
- [ ] **ReAct Pattern**: reasoning traces interleaved with actions
- [ ] **Planning**: breaking tasks into subtasks, decomposing goals
- [ ] **Memory**: short-term (conversation), long-term (persistent storage), working memory
- [ ] **Multi-Agent Systems**: agents collaborating, delegation, coordination
- [ ] **Error Handling**: tool failures, retries, graceful degradation
- [ ] **Safety Considerations**: sandboxing, permission models, human-in-the-loop
- [ ] **Evaluation**: measuring agent performance, benchmarking
- [ ] **Frameworks**: LangGraph, CrewAI, AutoGen, or building from scratch

## Practice Suggestions

1. **Build a search agent** — give an LLM access to a web search tool. Implement the ReAct loop: the LLM decides when to search, processes results, and reasons toward an answer.
2. **Multi-step planner** — build an agent that takes a high-level goal (e.g., "research Python async libraries and write a comparison") and breaks it into steps, executing each.

## Completion Checklist

- [ ] Can implement a basic agent loop (perceive → think → act)
- [ ] Understands tool definitions and tool call handling
- [ ] Can use ReAct-style prompting
- [ ] Has built an agent with at least 2 tools
- [ ] Understands the safety risks of autonomous agents
- [ ] Has experimented with multi-agent coordination
