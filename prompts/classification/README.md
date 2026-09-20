# Classification Prompts

Prompts for categorizing and labeling text.

## Prompt 1: Sentiment Analysis

**Purpose**: Classify text sentiment.

```
Classify the sentiment of the following text. Return as JSON.

Categories: positive, negative, neutral, mixed

For "mixed", provide both positive and negative aspects.

Text: {text}

Return: {"sentiment": "...", "confidence": 0.0-1.0, "reasoning": "..."}
```

**Variables**: `{text}` — the input text

**Example**:
```
Text: "The product quality is great but the shipping was terrible."

Output:
{
    "sentiment": "mixed",
    "confidence": 0.9,
    "reasoning": "Positive about product quality, negative about shipping experience."
}
```

**Tips**:
- Add domain-specific sentiment categories (e.g., "frustrated", "delighted")
- Provide examples for edge cases (sarcasm, irony)
- Calibrate confidence scores with test data

## Prompt 2: Topic Classification

**Purpose**: Classify text into predefined topics.

```
Classify the following text into one of these topics:

{topics}

If none fit well, use "other".

Text: {text}

Return: {"topic": "...", "confidence": 0.0-1.0}
```

**Variables**:
- `{topics}` — comma-separated list of topics
- `{text}` — the input text

**Example**:
```
Topics: technology, finance, health, sports, politics

Text: "The new iPhone features a faster processor and better camera."

Output:
{
    "topic": "technology",
    "confidence": 0.95
}
```

**Tips**:
- Keep topic list focused (5-10 topics max)
- Provide descriptions for ambiguous topics
- Add an "other" category for edge cases

## Prompt 3: Intent Classification

**Purpose**: Classify user intent from text.

```
Classify the user's intent from the following message.

Possible intents:
- question: asking for information
- request: asking for action
- complaint: expressing dissatisfaction
- feedback: providing opinions
- greeting: social opening
- goodbye: ending conversation
- other: none of the above

Message: {message}

Return: {"intent": "...", "confidence": 0.0-1.0, "entities": {...}}
```

**Variables**: `{message}` — the user message

**Example**:
```
Message: "Can you help me reset my password?"

Output:
{
    "intent": "request",
    "confidence": 0.95,
    "entities": {"action": "reset password"}
}
```

**Tips**:
- Customize intents for your application
- Extract relevant entities alongside intent
- Handle multi-intent messages
