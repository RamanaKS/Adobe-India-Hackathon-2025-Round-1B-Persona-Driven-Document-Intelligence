#!/bin/bash
# Usage: ./scripts/run_collection.sh Collection_1_Travel

COLLECTION_NAME=$1
COLLECTION_PATH="collections/${COLLECTION_NAME}"

if [ ! -d "$COLLECTION_PATH" ]; then
    echo "Collection $COLLECTION_NAME not found!"
    exit 1
fi

echo "Processing $COLLECTION_NAME..."

# Copy input to temp processing directory
cp "${COLLECTION_PATH}/challenge1b_input.json" temp_processing/current_input.json

# Update PDF paths in input JSON to point to correct collection
python scripts/update_pdf_paths.py temp_processing/current_input.json "$COLLECTION_PATH/PDFs"

# Run the document intelligence system
python src/document_intelligence.py temp_processing/current_input.json temp_processing/current_output.json

# Copy result back to collection
cp temp_processing/current_output.json "${COLLECTION_PATH}/challenge1b_output_generated.json"

echo "$COLLECTION_NAME processing completed!"