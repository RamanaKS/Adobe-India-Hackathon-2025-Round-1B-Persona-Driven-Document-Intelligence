#!/bin/bash
echo "Processing all collections..."

./scripts/run_collection.sh Collection_1_Travel
./scripts/run_collection.sh Collection_2_Adobe  
./scripts/run_collection.sh Collection_3_Recipe

echo "All collections processed!"