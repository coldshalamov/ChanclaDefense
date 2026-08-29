import re

with open('index.html', 'r') as f:
    content = f.read()

# Let's see the context around spawnChancla to add 'trick'
match = re.search(r'function spawnChancla.*?\{.*?return;', content, re.DOTALL)
if match:
    print(content[match.start():match.end()])
