import re

with open('index.html', 'r') as f:
    content = f.read()

idx = content.find('function spawnChancla')
if idx != -1:
    print(content[idx:idx+1500])
