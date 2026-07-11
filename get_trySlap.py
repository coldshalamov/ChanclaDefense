with open('index.html', 'r') as f:
    content = f.read()

import re

m = re.search(r'(const isPerfect = dist < perfectRange;\n\n\s+gameData\.stats\.totalSlaps\+\+;\n\s+if \(isPerfect\) gameData\.stats\.perfectSlaps\+\+;)', content)
print("Block trySlap:", bool(m))

m2 = re.search(r'(c\.slapped = true;\n\s+c\.vy = -600;\n\s+c\.vx = \(isa\.x - c\.x\) \* 1\.5;\n\s+c\.rotSpeed = 15;)', content)
print("Block trySlap 2:", bool(m2))
