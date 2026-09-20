# Benchmark Retrieval

A structured exercise: measure and improve your RAG retrieval quality.

## Steps

1. **Build a test set** — create 20 questions with known answers from your documents
2. **Measure** — for each question, check if retrieval finds the correct chunk
3. **Score** — calculate accuracy: correct chunks found / total questions
4. **Iterate** — change parameters and re-measure:
   - Chunk size: 200, 500, 1000, 2000 characters
   - Overlap: 0, 100, 200, 500 characters
   - Embedding model: try different models
5. **Report** — build a simple table of results

## Expected Output

A table like:

| Chunk Size | Overlap | Accuracy |
|-----------|---------|----------|
| 200       | 100     | 0.65     |
| 500       | 100     | 0.80     |
| 1000      | 100     | 0.85     |
| 2000      | 100     | 0.82     |
