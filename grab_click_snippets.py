import re

with open('index.html', 'r') as f:
    content = f.read()

click_match = re.search(r"else if \(pos\.y >= 560 && pos\.y <= 606 && pos\.x >= 110 && pos\.x <= canvas\.width - 110\) \{\n\s*setDirectionsVisible\(false\);\n\s*state = STATE\.COSMETICS;\n\s*\}\n\s*\} else if \(state === STATE\.SHOP\) \{", content)
if click_match:
    print(click_match.group(0))
