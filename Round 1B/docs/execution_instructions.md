# Setup
cd docker/
docker build -t docintel:1.0 .

# Run on a collection
docker run --rm -v /absolute/path/to/Collection_1_Travel:/data docintel:1.0 \
  /data/challenge1b_input.json /data/challenge1b_output.json

The container uses CPU only. The model (~500 MB) is downloaded on first run.

# Batch mode
Use `run_all_collections.sh` (shell script) to loop over collections and generate outputs.

# Validation
Use `python validate_outputs.py` to compare generated output files with expected ones (if available).
