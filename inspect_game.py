import re

with open('index.html', 'r') as f:
    content = f.read()

# Let's find update(dt)
update_idx = content.find('function update(dt)')
print("Found update at:", update_idx)
print(content[update_idx:update_idx+1000])
