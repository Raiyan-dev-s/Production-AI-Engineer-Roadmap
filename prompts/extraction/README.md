# Extraction Prompts

Prompts for extracting structured data from unstructured text.

## Prompt 1: Entity Extraction

**Purpose**: Extract named entities from text.

```
Extract all named entities from the following text. For each entity, provide:
- The entity text
- The entity type (PERSON, ORGANIZATION, LOCATION, DATE, etc.)
- The start and end position in the text

Text: {text}

Return as JSON with an "entities" array.
```

**Variables**: `{text}` — the input text

**Example**:
```
Text: "Apple Inc. was founded by Steve Jobs in Cupertino, California in 1976."

Output:
{
    "entities": [
        {"text": "Apple Inc.", "type": "ORGANIZATION", "start": 0, "end": 10},
        {"text": "Steve Jobs", "type": "PERSON", "start": 24, "end": 34},
        {"text": "Cupertino, California", "type": "LOCATION", "start": 38, "end": 59},
        {"text": "1976", "type": "DATE", "start": 63, "end": 67}
    ]
}
```

**Tips**:
- Customize entity types for your domain
- Add examples for domain-specific entities
- Handle edge cases (partial names, ambiguous dates)

## Prompt 2: Structured Data Extraction

**Purpose**: Extract structured data from free-form text into a specific schema.

```
Extract the following information from the text below. Return as JSON matching this schema:

{
    "name": "string",
    "email": "string or null",
    "company": "string or null",
    "role": "string or null",
    "location": "string or null",
    "skills": ["string"]
}

Text: {text}

If a field is not found, use null. Extract all skills mentioned, even if implied.
```

**Variables**: `{text}` — the input text

**Example**:
```
Text: "I'm Sarah Chen, a ML engineer at Google based in NYC. I work with PyTorch and transformers."

Output:
{
    "name": "Sarah Chen",
    "email": null,
    "company": "Google",
    "role": "ML engineer",
    "location": "NYC",
    "skills": ["PyTorch", "transformers"]
}
```

**Tips**:
- Define the schema clearly in the prompt
- Provide examples of edge cases (missing fields)
- Use Pydantic to validate the output

## Prompt 3: Key-Value Extraction

**Purpose**: Extract key-value pairs from text.

```
Extract all key-value pairs from the following text. Return as a JSON object.

Rules:
- Keys should be normalized (lowercase, snake_case)
- Values should preserve their original format
- If a value is a list, use a JSON array
- If a value is numeric, use the number type (not string)

Text: {text}
```

**Variables**: `{text}` — the input text

**Example**:
```
Text: "Order #12345 placed on January 15, 2024. Total: $156.78. Items: Widget A (x3), Widget B (x1)"

Output:
{
    "order_number": "12345",
    "date": "January 15, 2024",
    "total": "$156.78",
    "items": ["Widget A (x3)", "Widget B (x1)"]
}
```

**Tips**:
- Define normalization rules for keys
- Handle nested structures
- Test with varied input formats
