import re

with open('index.html', 'r') as f:
    content = f.read()

draw_match = re.search(r"function drawCosmetics\(\) \{", content)
if draw_match:
    print(draw_match.group(0))
