import re

with open('index.html', 'r') as f:
    content = f.read()

idx = content.find('for (let i = chanclas.length - 1; i >= 0; i--)')
# Wait, this loop is inside trySlap()!
# The update loop must be somewhere else.
idx2 = content.find('chanclas = chanclas.filter(c =>')
if idx2 != -1:
    print("Found filter:", content[idx2-1500:idx2+500])
