import re

with open('index.html', 'r') as f:
    content = f.read()

idx = content.find('for (let i = chanclas.length - 1; i >= 0; i--)')
idx2 = content.find('for (let i = chanclas.length - 1; i >= 0; i--)', idx + 1)
print("Second loop at:", idx2)

print(content[idx2-500:idx2+1500])
