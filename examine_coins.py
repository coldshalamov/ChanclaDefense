import re

for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    print(f"=== {filename} COINS ===")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'gameData.coins +=' in line:
            print(f"{i+1}: {line.strip()}")

    print(f"=== {filename} SCORE ===")
    for i, line in enumerate(lines):
        if 'score +=' in line:
            print(f"{i+1}: {line.strip()}")
