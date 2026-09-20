# RAG Prompts

Prompts for retrieval-augmented generation — answering questions based on retrieved context.

## Prompt 1: Context-Aware QA

**Purpose**: Answer questions based on provided context.

```
You are a helpful assistant. Answer the question based ONLY on the provided context.

Rules:
- If the context doesn't contain the answer, say "I don't have enough information to answer this question."
- Don't make up information not in the context.
- Cite which part of the context supports your answer.

Context:
{context}

Question: {question}

Answer:
```

**Variables**:
- `{context}` — retrieved document chunks
- `{question}` — the user's question

**Example**:
```
Context:
Chunk 1: Python 3.12 was released in October 2023. It includes performance improvements...
Chunk 2: The GIL (Global Interpreter Lock) prevents true parallel execution of threads...

Question: "What's new in Python 3.12?"

Answer:
Python 3.12 was released in October 2023 and includes performance improvements [Chunk 1].
```

**Tips**:
- Test with questions that have no answer in context
- Add instructions for handling conflicting information
- Consider adding source references

## Prompt 2: Multi-Turn with Context

**Purpose**: Handle multi-turn conversations with RAG.

```
You are a helpful assistant with access to the following documents:

{context}

Conversation history:
{history}

Answer the latest user message based on the context and conversation history.
If the context doesn't contain relevant information, say so.
If the user asks a follow-up question, use the conversation history to understand references.

User: {message}
Assistant:
```

**Variables**:
- `{context}` — retrieved document chunks
- `{history}` — conversation history
- `{message}` — the latest user message

**Example**:
```
Context:
Chunk 1: FastAPI is a modern web framework for Python...
Chunk 2: Pydantic is a data validation library...

History:
User: What is FastAPI?
Assistant: FastAPI is a modern web framework for Python...

User: What about validation?

Answer:
For validation, FastAPI uses Pydantic, a data validation library [Chunk 2].
```

**Tips**:
- Limit context window size
- Handle context changes between turns
- Track which chunks have been cited

## Prompt 3: RAG with Citations

**Purpose**: Answer questions with explicit source citations.

```
Answer the question using the provided sources. For each claim, cite the source using [Source N].

Sources:
{sources}

Rules:
- Every factual claim must cite a source
- If sources conflict, mention both perspectives
- If the answer isn't in the sources, say so clearly
- List all sources used at the end

Question: {question}
```

**Variables**:
- `{sources}` — numbered source chunks
- `{question}` — the user's question

**Tips**:
- Use consistent source numbering
- Test citation accuracy
- Handle multiple sources for the same claim
