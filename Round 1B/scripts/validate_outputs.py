import json
import sys
from difflib import unified_diff

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_outputs(ref_path, gen_path):
    try:
        ref = load_json(ref_path)
        gen = load_json(gen_path)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    if ref == gen:
        print("Outputs match exactly!")
        return

    print("Differences found between reference and generated outputs:\n")
    ref_str = json.dumps(ref, indent=2, sort_keys=True)
    gen_str = json.dumps(gen, indent=2, sort_keys=True)

    diff = unified_diff(
        ref_str.splitlines(), gen_str.splitlines(),
        fromfile='Expected', tofile='Generated',
        lineterm=''
    )

    for line in diff:
        print(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_outputs.py reference.json generated.json")
        sys.exit(1)

    validate_outputs(sys.argv[1], sys.argv[2])
