import re

for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    # Search for gameData initialization
    match = re.search(r'let gameData = \{.*?\}', content)
    print(f"{filename}: gameData = {match.group(0) if match else 'Not found'}")

    # Find where to insert PRESTIGE state
    match = re.search(r'const STATE = \{.*?\}', content)
    print(f"{filename}: STATE = {match.group(0) if match else 'Not found'}")
