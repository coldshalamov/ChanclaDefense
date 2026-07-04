import re

with open('index.html', 'r') as f:
    content = f.read()

# I need to add PRESTIGE state, buttons, multipliers.
# Let's check `score += ` lines again.
score_matches = re.finditer(r'score \+= ([^;]+);', content)
for m in score_matches:
    print(m.group(0))

print("----")
coin_matches = re.finditer(r'gameData\.coins \+= ([^;]+);', content)
for m in coin_matches:
    print(m.group(0))
