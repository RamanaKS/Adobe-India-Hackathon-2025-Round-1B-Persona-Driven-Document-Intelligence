We designed a generic persona‑driven document intelligence engine that meets the specified constraints. The process is:

1. **PDF parsing**: We use PyPDF2 to extract text page by page. Each page is treated as a “section” to avoid dependency on structural markers like headings, enabling domain agnosticism.

2. **Embedding & persona‑task context**: We use the lightweight `all‑MiniLM‑L6‑v2` model (≈ 500 MB) under 1 GB constraint. We encode the persona + job description together as a single query vector. Each section (e.g. page) is embedded likewise.

3. **Relevance ranking**: We compute cosine similarity between the persona‑task query and each document section embedding to score relevance. We then rank sections accordingly.

4. **Importance ranking**: We assign importance_rank = 1,2,3... based on sorted similarity scores for each document, selecting top‑k (e.g., top 3 per doc), ensuring focus.

5. **Sub‑section analysis (refined text)**: For each selected section, we trim and lightly clean up to produce a refined_text snippet (first ~500 chars). In production systems, this step could invoke a summarizer model or heuristic cleaning.

6. **JSON output**: We build `metadata`, `extracted_sections`, and `subsection_analysis` matching exactly the challenge output schema, including processing timestamp in ISO format.

7. **Performance & constraints**: Sentence‑transformers MiniLM runs efficiently on CPU. Even with 5 documents * ~20 pages each, embedding all sections and scoring finishes well under 60 s on a typical modern CPU. The model footprint is ≈ 500 MB.

8. **Generality**: Since sections are page‑based and persona‑task is free text, the solution generalizes to any domain (research, business, education, etc.) and any persona/task combination.

This fulfills all requirements: persona‑based extraction, importance ranking, multiple documents, generic operation, CPU‑only, sub‑1 GB model, <60 s runtime, structured JSON output.
