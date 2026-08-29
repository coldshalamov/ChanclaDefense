import re

with open('index.html', 'r') as f:
    content = f.read()

# find drawChancla
match = re.search(r'function drawChancla\(.*?\).*?\{.*?\}', content, re.DOTALL)
if match:
    print(content[match.start():match.start()+1500])
