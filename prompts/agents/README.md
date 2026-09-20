# Agent Prompts

Prompts for agent reasoning, planning, and tool use.

## Prompt 1: ReAct Reasoning

**Purpose**: Implement ReAct (Reason + Act) pattern.

```
You are a helpful assistant that can use tools to answer questions.

Available tools:
{tools}

Use the following format:
Thought: [your reasoning about what to do next]
Action: [tool name]
Action Input: [input for the tool]

When you have enough information to answer:
Thought: I now have enough information to answer the question
Answer: [your final answer]

Question: {question}
```

**Variables**:
- `{tools}` — list of available tools with descriptions
- `{question}` — the user's question

**Example**:
```
Available tools:
- search(query): Search the web for information
- calculator(expression): Evaluate a mathematical expression

Question: "What is the population of France divided by 2?"

Thought: I need to find the population of France first
Action: search
Action Input: population of France 2024

Observation: France has a population of approximately 68 million

Thought: Now I need to divide this by 2
Action: calculator
Action Input: 68000000 / 2

Observation: 34000000

Thought: I now have enough information to answer the question
Answer: The population of France divided by 2 is approximately 34 million.
```

**Tips**:
- Provide clear tool descriptions
- Handle tool errors gracefully
- Limit the number of reasoning steps

## Prompt 2: Planning

**Purpose**: Break complex tasks into steps.

```
You are a planning assistant. Given a goal, break it down into concrete steps.

Rules:
- Each step should be actionable and specific
- Steps should be in logical order
- Include dependencies between steps
- Estimate complexity (easy/medium/hard)

Goal: {goal}

Return a JSON plan:
{
    "steps": [
        {
            "id": 1,
            "description": "...",
            "dependencies": [],
            "complexity": "easy|medium|hard"
        }
    ]
}
```

**Variables**: `{goal}` — the high-level goal

**Example**:
```
Goal: "Build a REST API for user management"

Output:
{
    "steps": [
        {"id": 1, "description": "Define data models (User, Role)", "dependencies": [], "complexity": "easy"},
        {"id": 2, "description": "Set up database connection and migrations", "dependencies": [1], "complexity": "medium"},
        {"id": 3, "description": "Implement CRUD endpoints", "dependencies": [1, 2], "complexity": "medium"},
        {"id": 4, "description": "Add authentication", "dependencies": [3], "complexity": "hard"},
        {"id": 5, "description": "Write tests", "dependencies": [3], "complexity": "medium"},
        {"id": 6, "description": "Add documentation", "dependencies": [3], "complexity": "easy"}
    ]
}
```

**Tips**:
- Break down "hard" steps further
- Identify critical path
- Add validation steps

## Prompt 3: Tool Selection

**Purpose**: Choose the right tool for a task.

```
You have access to the following tools:

{tools}

Given a task, select the most appropriate tool and explain why.

If no tool is appropriate, say "No tool needed" and explain why.

Task: {task}

Return:
{
    "tool": "...",
    "reasoning": "...",
    "input": "..."
}
```

**Variables**:
- `{tools}` — list of tools with descriptions
- `{task}` — the task to accomplish

**Tips**:
- Include tool limitations in descriptions
- Handle ambiguous tasks
- Consider tool chaining when needed
