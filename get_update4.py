import re

with open('index.html', 'r') as f:
    content = f.read()

idx = content.find('// Update chancla positions')
if idx != -1:
    print(content[idx:idx+2500])
