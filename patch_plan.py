with open("index.html", "r") as f:
    content = f.read()

import re

# We will print the sections we want to modify.

print("--- trySlap ---")
match = re.search(r'(c\.vx = \(c\.x - player\.x\) \* \(isPerfect \? 12 : 8\);\s*c\.vy = isPerfect \? -550 : -300;\s*c\.slapped = true;)', content)
if match:
    print(match.group(1))
