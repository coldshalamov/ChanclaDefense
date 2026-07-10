import re

with open('index.html', 'r') as f:
    content = f.read()

idx = content.find('for (let i = chanclas.length - 1; i >= 0; i--) {')
if idx != -1:
    print(content[idx:idx+1500])
