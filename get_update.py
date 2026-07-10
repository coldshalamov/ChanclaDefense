import re

with open('index.html', 'r') as f:
    content = f.read()

idx = content.find('chanclas.forEach((c, index) => {')
if idx != -1:
    print(content[idx:idx+1500])
