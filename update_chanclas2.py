import re
with open('index.html', 'r') as f:
    content = f.read()

# find updateChanclas
match = re.search(r'function updateChanclas\(.*?\).*?function ', content, re.DOTALL)
if match:
    print(content[match.start():match.start()+2500])
