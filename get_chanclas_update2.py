import re

with open('index.html', 'r') as f:
    content = f.read()

# Let's search for "c.y +=" or "c.x +="
for m in re.finditer(r'c\.[xy] \+=', content):
    start = max(0, m.start() - 200)
    end = min(len(content), m.end() + 200)
    print("Match at", m.start(), "...")
    # Just print the first one or two
    break

idx = content.find('chanclas.length')
for i in range(10):
    idx = content.find('chanclas.length', idx + 1)
    if idx == -1: break
    print("Found length at", idx)
