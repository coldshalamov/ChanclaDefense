import re

with open('index.html', 'r') as f:
    content = f.read()

# I need to find where to add `isBlackhole`.
# Let's search `function spawnChancla`
idx = content.find('function spawnChancla')
print("Spawn chancla:\n", content[idx:idx+800])
