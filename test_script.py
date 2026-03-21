import re

with open('index.html', 'r') as f:
    content = f.read()

print(content[content.find('function drawTitleScreen'):content.find('function drawGameOver')])
