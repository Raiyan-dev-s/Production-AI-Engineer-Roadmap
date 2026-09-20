# Experiments

## What Are Experiments?

Experiments are for testing ideas, trying new models, comparing approaches, and prototyping — without affecting production code.

## Experiments vs Production Code

| Experiments | Production Code |
|------------|----------------|
| Throwaway is fine | Must be maintained |
| Hardcoded values OK | Configuration-driven |
| Print statements OK | Structured logging |
| Skip error handling | Handle all errors |
| Skip tests | Tests required |
| Quick and dirty | Clean and documented |

## Organization

```
experiments/
├── README.md              ← you are here
├── model-comparison/      ← compare LLM performance
├── prompt-templates/      ← try different prompt approaches
├── rag-prototypes/        ← test RAG configurations
└── agent-patterns/        ← prototype agent architectures
```

## Naming Convention

Each experiment gets its own directory with a descriptive name:

```
experiments/
├── 2024-01-model-cost-analysis/
├── 2024-02-chunk-size-benchmark/
└── 2024-03-agent-tool-use/
```

Include date prefix for chronological ordering.

## Experiment Template

Create a `README.md` in each experiment directory:

```markdown
# [Experiment Name]

## Hypothesis
What are you testing?

## Setup
How to reproduce the experiment.

## Results
What did you find?

## Conclusions
What should we do based on the results?

## Next Steps
What should we try next?
```

## When to Promote to Production

Move experiment code to production when:
- The approach is proven to work
- It has been tested with real data
- It handles edge cases
- It has proper error handling
- It has been code reviewed

## Tips

- **Time-box experiments** — set a deadline and stick to it
- **Document everything** — future you will forget why you tried something
- **Keep experiments small** — one variable at a time
- **Use real data** — synthetic data can be misleading
- **Share results** — tell the team what you learned
