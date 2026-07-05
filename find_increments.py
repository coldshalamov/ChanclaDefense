import re

def find_lines(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if 'score +=' in line or 'gameData.coins +=' in line or 'totalCoinsEarned +=' in line:
                print(f"{filename}:{i+1}: {line.strip()}")

find_lines('index.html')
