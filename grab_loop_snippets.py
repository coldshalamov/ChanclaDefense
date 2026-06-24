import re

with open('index.html', 'r') as f:
    content = f.read()

loop_match = re.search(r"else if \(state === STATE\.COSMETICS\) drawCosmetics\(\);\n\s*else if \(state === STATE\.WIN\)", content)
if loop_match:
    print(loop_match.group(0))
