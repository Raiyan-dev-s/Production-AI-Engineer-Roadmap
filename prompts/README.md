# Prompt Library

A collection of reusable prompt templates organized by use case.

## Structure

```
prompts/
├── README.md           ← you are here
├── system/             ← system prompts for different roles
├── extraction/         ← entity and data extraction
├── classification/     ← categorization and labeling
├── rag/                ← retrieval-augmented generation
└── agents/             ← agent reasoning and planning
```

## How to Use

1. **Browse by category** — find the prompt type that matches your need
2. **Copy and adapt** — customize the template for your specific use case
3. **Version control** — track prompt changes in git
4. **Test prompts** — evaluate with real inputs before using in production

## Prompt Template Format

Each prompt file includes:
- **Purpose** — what the prompt does
- **Variables** — placeholders to fill in
- **Example** — a worked example
- **Tips** — guidance for customization

## Creating New Prompts

When adding prompts to this library:

1. Use the template format (purpose, variables, example, tips)
2. Include the model you tested with
3. Document expected input/output formats
4. Note any edge cases you discovered

## Tips for Good Prompts

- **Be specific** — vague prompts get vague results
- **Provide context** — give the LLM what it needs to succeed
- **Define output format** — JSON, markdown, plain text
- **Use examples** — show, don't just tell
- **Test adversarial inputs** — try to break your prompts
- **Version everything** — track what works and what doesn't
