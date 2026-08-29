import re
with open('index.html', 'r') as f:
    content = f.read()

# Let's find trickState
match = re.search(r'c.trickState', content)
if match:
    print("trickState found!")
else:
    print("trickState NOT found.")
