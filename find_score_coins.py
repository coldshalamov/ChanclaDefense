import re

with open('index.html', 'r') as f:
    content = f.read()

# Find score additions
for m in re.finditer(r'score \+= [^;]+;', content):
    print("Score logic:", m.group(0))

# Find coin additions
for m in re.finditer(r'gameData\.coins \+= [^;]+;', content):
    print("Coins logic:", m.group(0))
