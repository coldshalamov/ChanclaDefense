import re

with open('index.html', 'r') as f:
    content = f.read()

drawTitleMatch = re.search(r'function drawTitleScreen\(\) \{.*?(?=function)', content, re.DOTALL)
if drawTitleMatch:
    print(drawTitleMatch.group(0))
