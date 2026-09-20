# LLM Fundamentals

## What to Learn

Understanding Large Language Models from a practitioner's perspective — how to use them, not how to train them.

## Why It Matters

LLMs are the core of modern AI applications. Knowing how to interact with them effectively — and economically — is essential.

## Concepts Checklist

- [ ] **What LLMs Are**: transformer architecture basics, capabilities vs limitations
- [ ] **Tokens & Tokenization**: how text is split, token counting, cost implications
- [ ] **Prompts & Completions**: system/user/assistant message roles, temperature, max tokens
- [ ] **API Usage**: OpenAI API, Anthropic API, litellm for provider abstraction
- [ ] **Prompt Engineering**: zero-shot, few-shot, chain-of-thought, structured output
- [ ] **Streaming**: streaming completions, handling partial responses
- [ ] **Function Calling**: tool definitions, structured function calls, parallel tool use
- [ ] **Model Selection**: capability trade-offs, cost vs quality, when to use smaller models
- [ ] **Cost Management**: token pricing, caching completions, optimizing prompt length
- [ ] **Evaluation**: how to judge output quality, building evaluation datasets
- [ ] **Hallucination**: what it is, why it happens, mitigation strategies
- [ ] **Safety**: content filtering, PII handling, prompt injection risks

## Practice Suggestions

1. **Compare models** — send the same 10 prompts to GPT-4o, Claude, and a smaller model. Build a simple scoring rubric and evaluate output quality and latency.
2. **Build a cost tracker** — wrap LLM API calls to log tokens used, cost, and latency. Run a batch of 100 prompts and generate a cost report.

## Completion Checklist

- [ ] Can use OpenAI/Anthropic APIs to get completions
- [ ] Understands token counting and its impact on cost
- [ ] Can write effective system and user prompts
- [ ] Has experimented with streaming responses
- [ ] Understands function calling / tool use
- [ ] Can articulate trade-offs between models
- [ ] Knows what hallucination is and how to mitigate it
