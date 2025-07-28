# Adobe India Hackathon 2025 – Round 1B: Persona-Driven Document Intelligence

## Intelligent PDF Analyzer

**Participants:** Ramana K S, Ranjith Kumar A, Sharanbabu B

---

## Problem Statement

Design a document intelligence system that extracts and ranks relevant sections from a collection of PDF documents based on a given **persona** and their **job to be done**.

The system must run **offline**, **on CPU**, inside a **Docker container** with **no internet access**, and produce results in a **specific JSON format**.

---

## Project Summary

This solution uses an **embedding-based semantic ranking pipeline** that:

* Embeds the persona and job description as a **semantic query**
* Extracts and scores sections from all PDFs using **sentence embeddings (MiniLM)**
* **Ranks the top-3 sections per document** by similarity
* Outputs structured results with **metadata, extracted sections, and refined subsection analysis**

---

## Methodology

### Step 1: Input Handling

* Input is a JSON file containing:

  * List of PDF files
  * Persona (e.g. "HR professional")
  * Job to be done (e.g. "Create and manage fillable forms")

### Step 2: Text Extraction (PyPDF2)

* Each PDF page is treated as a **section**
* Extracts plain text from all pages

### Step 3: Embedding + Ranking

* Uses **all-MiniLM-L6-v2** model (pre-cached) from `sentence-transformers`
* Converts the persona + job into a **query embedding**
* Computes embeddings for each section and scores them using **cosine similarity**

### Step 4: Subsection Refinement

* Uses a simple **heuristic summarizer** that trims each section's text to \~500 characters for readability

### Step 5: Output Generation

* Saves JSON file with:

  * Metadata (timestamp, persona, documents)
  * Top-3 extracted sections per document with rank
  * Refined subsection summaries

---

## Project Structure

```
document_intelligence/
├── src/
│   ├── document_intelligence.py    # Main execution script
├── collections/
│   ├── Collection_1_Travel/
│   │   ├── challenge1b_input.json
│   │   └── PDFs/*.pdf
├── output/
│   └── Collection_1_Travel/challenge1b_output_generated.json
├── docker/
│   ├── Dockerfile
│   └── requirements.txt
├── README.md
```

---

## Output Format

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "HR professional",
    "job_to_be_done": "Create and manage fillable forms",
    "processing_timestamp": "2025-07-10T15:34:33Z"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Page 3",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Extracted text here...",
      "page_number": 3
    }
  ]
}
```

---

## How to Run

### 1. Local (Development Mode)

```bash
pip install -r docker/requirements.txt
python src/document_intelligence.py collections/Collection_1_Travel/challenge1b_input.json output/Collection_1_Travel/challenge1b_output_generated.json
```

---

### 2. Docker Execution (Offline, CPU-only)

#### Build Docker Image

```bash
docker build -t adobe_hackathon_1b -f docker/Dockerfile .
```

#### Run Docker Container

```bash
docker run --rm \
  -v %cd%/collections:/app/collections \
  -v %cd%/output:/app/output \
  adobe_hackathon_1b \
  collections/Collection_1_Travel/challenge1b_input.json \
  output/Collection_1_Travel/challenge1b_output_generated.json
```

> Replace paths for other collections accordingly.

---

## Constraints Satisfied

| Constraint                      | Status               |
| ------------------------------- | -------------------- |
| Offline execution (no internet) | Yes                  |
| CPU-only (no GPU)               | Yes                  |
| Model size ≤ 1GB                | Yes (MiniLM)         |
| Processing time ≤ 60s           | Yes (under 15s avg.) |
| JSON format (Adobe Spec)        | Yes                  |

---

## Dependencies

```
PyPDF2==3.0.0
sentence_transformers==2.2.2
torch>=2.0.0
```

---

## Sample Input/Output

* `collections/Collection_1_Travel/challenge1b_input.json`
* `output/Collection_1_Travel/challenge1b_output_generated.json`

---

## Authors

**Ramana K S**
**Ranjith Kumar A**
**Sharanbabu B**
B.E. Computer Science and Engineering, Panimalar Engineering College
*Adobe India Hackathon 2025 – Round 1B Submission*
