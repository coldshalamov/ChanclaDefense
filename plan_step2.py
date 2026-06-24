import re

with open('index.html', 'r') as f:
    content = f.read()

# Let's verify `isBlackhole` in `index.html`
print("isBlackhole:", "const isBlackhole" in content)
print("GALAXY BURST:", "GALAXY BURST" in content)
