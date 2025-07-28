import os, json, time
from dataclasses import dataclass
from typing import List
import pathlib
import PyPDF2
from sentence_transformers import SentenceTransformer, util

@dataclass
class Document:
    filename: str
    title: str
    texts: List[str]
    sections: List[dict]

def load_input(path):
    with open(path, 'r', encoding='utf‑8') as f:
        return json.load(f)

def extract_text_and_sections(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    texts = []
    sections = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        texts.append(text)
        # naive split: each page is a "section"
        sections.append({
            'page_number': i + 1,
            'section_title': f"Page {i+1}",
            'raw_text': text
        })
    return texts, sections

def compute_embeddings(sections, model):
    texts = [sec['raw_text'] or "" for sec in sections]
    return model.encode(texts, convert_to_tensor=True, show_progress_bar=False)

def rank_sections(sections, embeddings, query_emb):
    scores = util.pytorch_cos_sim(query_emb, embeddings)[0]
    ranked = sorted(
        zip(sections, scores.tolist()),
        key=lambda x: x[1],
        reverse=True
    )
    return [(sec, float(score)) for sec, score in ranked]

def refine_text(raw_text):
    # Placeholder: could use GPT‑style summarizer or heuristic trim
    # Here just trim to first 500 characters
    return raw_text.strip().replace('\n', ' ')[:500] + ('…' if len(raw_text)>500 else '')

def process_collection(input_json_path):
    inp = load_input(input_json_path)
    persona = inp['persona']['role']
    job = inp['job_to_be_done']['task']
    docs_meta = inp['documents']
    documents = []
    for d in docs_meta:
        fp = os.path.join(os.path.dirname(input_json_path), 'PDFs', d['filename'])
        texts, sections = extract_text_and_sections(fp)
        documents.append(Document(filename=d['filename'], title=d.get('title', d['filename']), texts=texts, sections=sections))

    model = SentenceTransformer('all-MiniLM-L6-v2')
    query = f"Persona: {persona}. Task: {job}."
    query_emb = model.encode(query, convert_to_tensor=True)
    output = {
        "metadata": {
            "input_documents": [d.filename for d in documents],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for doc in documents:
        embeddings = compute_embeddings(doc.sections, model)
        ranked = rank_sections(doc.sections, embeddings, query_emb)
        # take top‑3 sections per doc
        for rank, (sec, score) in enumerate(ranked[:3], start=1):
            output["extracted_sections"].append({
                "document": doc.filename,
                "section_title": sec['section_title'],
                "page_number": sec['page_number'],
                "importance_rank": rank
            })
            refined = refine_text(sec['raw_text'])
            output["subsection_analysis"].append({
                "document": doc.filename,
                "refined_text": refined,
                "page_number": sec['page_number']
            })

    return output

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", help="path to challenge1b_input.json")
    parser.add_argument("output_json", help="full path where output JSON should be saved")
    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output_json)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    result = process_collection(args.input_json)

    with open(args.output_json, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Output written to: {args.output_json}")

