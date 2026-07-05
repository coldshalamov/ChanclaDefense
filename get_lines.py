import re
with open('index.html', 'r') as f:
    for i, line in enumerate(f):
        if 'else if (state === STATE.COSMETICS) {' in line:
            print(f"{i+1}: {line.strip()}")
        if 'if (state === STATE.COSMETICS) {' in line:
            print(f"{i+1}: {line.strip()}")
        if 'ctx.fillText(\'Boss Bonus:' in line:
            print(f"{i+1}: {line.strip()}")
        if 'else if (pos.y >= 560' in line:
            print(f"{i+1}: {line.strip()}")
