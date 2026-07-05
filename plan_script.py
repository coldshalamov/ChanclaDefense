import re

with open("index.html", "r") as f:
    content = f.read()

# Let's verify what the end of the canvas click listener for COSMETICS really looks like.
match = re.search(r"// Check Back Button\n                    if \(pos\.y >= canvas\.height - 80 && pos\.y <= canvas\.height - 30 && pos\.x >= 100 && pos\.x <= canvas\.width - 100\) \{\n                        setDirectionsVisible\(true\);\n                        state = STATE\.TITLE;\n                    \}\n                \}", content, re.DOTALL)
if match:
    print("Found match! " + match.group(0))
else:
    print("No match found for end of STATE.COSMETICS click handler.")

match2 = re.search(r"else if \(state === STATE\.COSMETICS\) \{.*?\n                \}", content, re.DOTALL)
if match2:
    print(match2.group(0)[-200:])
