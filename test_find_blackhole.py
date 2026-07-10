import re

with open('index.html', 'r') as f:
    content = f.read()

print("Type blackhole:", 'blackhole' in content)
