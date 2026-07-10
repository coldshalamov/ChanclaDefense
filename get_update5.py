import re

with open('index.html', 'r') as f:
    content = f.read()

idx = content.find('chanclas.forEach(')
if idx != -1:
    print(content[idx:idx+2500])
else:
    # try for loop
    idx2 = content.find('for (let i = chanclas.length - 1; i >= 0; i--)')
    if idx2 != -1:
        # Before this loop is probably the position updates.
        print(content[idx2-1000:idx2+1000])
