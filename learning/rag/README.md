# Retrieval Augmented Generation (RAG)

## What to Learn

How to ground LLM responses in your own data — the key technique for building AI that knows your documents.

## Why It Matters

LLMs without RAG are generalists. With RAG, they become specialists that can answer questions about your specific data, without fine-tuning.

## Concepts Checklist

- [ ] **Why RAG**: limitations of LLM-only approaches, when to use RAG vs fine-tuning
- [ ] **Document Loading**: reading PDFs, HTML, markdown, structured data
- [ ] **Text Splitting**: chunking strategies, overlap, impact on retrieval quality
- [ ] **Embeddings**: converting text to vectors, embedding models, dimensionality
- [ ] **Vector Stores**: storing embeddings, similarity search, FAISS/Chroma basics
- [ ] **Retrieval**: finding relevant chunks, similarity metrics, re-ranking
- [ ] **Generation**: passing context to LLM, prompt templates, citation
- [ ] **RAG Pipelines**: LangChain/LlamaIndex for orchestration
- [ ] **Evaluation**: measuring retrieval quality, building evaluation datasets
- [ ] **Advanced RAG**: query transformation, hybrid search, multi-modal RAG

## Practice Suggestions

1. **RAG over your notes** — build a Q&A system over a collection of your own documents. Load, split, embed, store, retrieve, generate. Compare RAG answers to LLM-only answers.
2. **Benchmark retrieval** — build a set of 20 questions with known answers. Measure how often your retrieval finds the right chunk. Iterate on chunk size and overlap.

## Completion Checklist

- [ ] Can load and split documents for RAG
- [ ] Understands embedding generation and vector storage
- [ ] Can build a basic RAG pipeline
- [ ] Has compared RAG vs LLM-only answers
- [ ] Knows how to evaluate retrieval quality
- [ ] Understands the impact of chunk size on quality
