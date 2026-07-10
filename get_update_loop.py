import re

with open('index.html', 'r') as f:
    content = f.read()

idx = content.find('function update(dt)')
print(content[idx:idx+3500])
