import json
import os
import sys

def update_pdf_paths(input_json_path, pdf_dir_path):
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for doc in data.get("documents", []):
        filename = doc.get("filename", "")
        full_path = os.path.join(pdf_dir_path, filename)
        if not os.path.exists(full_path):
            print(f"Warning: PDF not found: {full_path}")
        doc["filename"] = full_path

    with open(input_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_pdf_paths.py input_json_path pdf_directory")
        sys.exit(1)

    update_pdf_paths(sys.argv[1], sys.argv[2])
    print(f"PDF paths updated in {sys.argv[1]}")
