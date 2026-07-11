with open('index.html', 'r') as f:
    content = f.read()

import re

# Block 10
m10 = re.search(r'(function addFloatText\(text, x, y, color = \'#fff\', fontSize = 14\) \{\n\s+floatTexts\.push\(\{ text, x, y, time: 1\.8, max: 1\.8, color, fontSize \}\);\n\s+\})', content)
print("Block 10:", bool(m10))

# Block 11
m11 = re.search(r'(function drawFloatTexts\(\) \{\n\s+floatTexts\.forEach\(f => \{\n\s+ctx\.save\(\);\n\s+ctx\.globalAlpha = Math\.max\(0, f\.time / f\.max\);\n\s+ctx\.fillStyle = \'#fff\';\n\s+ctx\.font = \'14px sans-serif\';\n\s+ctx\.textAlign = \'center\';)', content)
print("Block 11:", bool(m11))

# Block 12
m12 = re.search(r'(let hitStop = 0;\n\s+let meteorTimer = 0;)', content)
print("Block 12:", bool(m12))

# Block 13
m13 = re.search(r'(if \(hitStop > 0\) \{\n\s+hitStop -= dt;\n\s+return;\n\s+\})', content)
print("Block 13:", bool(m13))
