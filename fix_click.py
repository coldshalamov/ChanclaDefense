import re

with open('index.html', 'r') as f:
    content = f.read()

# Let's check how the exact y coords for prestige in Title match up
match = re.search(r'pos\.y >= 620 && pos\.y <= 666', content)
if match:
    print("Found Title prestige hitboxes")
else:
    print("Missing title prestige hitbox!")

match2 = re.search(r'pos\.y >= 300 && pos\.y <= 360', content)
if match2:
    print("Found Prestige confirm hitbox")
else:
    print("Missing confirm hitbox")
