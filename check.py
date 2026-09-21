import re

with open('index.html', 'r') as f:
    content = f.read()

# Check drawChancla
print("drawChancla:", "function drawChancla(ctx, x, y, w, h, type, rotation)" in content)
print("drawChanclasAll:", "function drawChanclasAll()" in content)
print("trySlap:", "c.type === 'trick'" in content)
