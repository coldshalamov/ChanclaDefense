#!/bin/bash
for file in verification/*.py; do
    echo "Running $file..."
    python3.12 "$file" || break
done
