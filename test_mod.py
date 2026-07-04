import re

with open('index.html', 'r') as f:
    content = f.read()

# Let's inspect where STATE.PRESTIGE might have existed
print("Checking for prestige...")
if "STATE.PRESTIGE" in content:
    print("Prestige state exists!")
else:
    print("No prestige state.")
