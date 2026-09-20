# RAG Over Your Notes

A hands-on exercise: build a Q&A system over your own documents.

## Steps

1. **Collect** — gather 20-50 pages of your own documents (PDFs, markdown, notes)
2. **Load** — read documents using a document loader
3. **Split** — chunk documents into 500-1000 character segments with 100-200 character overlap
4. **Embed** — convert text chunks to vectors using an embedding model
5. **Store** — save vectors in a vector store (FAISS, Chroma)
6. **Retrieve** — given a question, find the most similar chunks
7. **Generate** — pass retrieved chunks and the question to an LLM to generate an answer
8. **Compare** — ask the same question without RAG (LLM-only) and compare answers

## Key Questions to Ask

- Can the LLM answer questions about your specific data without RAG?
- How does RAG answer quality compare to LLM-only?
- What happens when you change chunk size (200, 500, 1000, 2000 characters)?
- What happens when you change overlap (0, 100, 200, 500 characters)?
