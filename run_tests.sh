for f in verification/verify_*.py; do
    echo "Running $f..."
    python "$f"
done
