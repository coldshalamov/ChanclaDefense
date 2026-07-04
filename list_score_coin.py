import re

with open('index.html', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'score +=' in line or 'gameData.coins +=' in line:
        print(f"Line {i+1}: {line.strip()}")
