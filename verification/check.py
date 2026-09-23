import re

def get_blocks(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # block 1: spawnChancla
    b1 = re.search(r"const isSniper.*?0\.12;[\s\S]*?const isFire = isa.enraged.*?;", content).group(0)
    print("--- Block 1 (spawnChancla) ---")
    print(b1)

    b2 = re.search(r"else if \(isTrick\) \{ w = 36; h = 22; \}\n.*?else if \(isSniper\) \{ w = 34; h = 24; \}", content).group(0)
    print("--- Block 2 (spawn sizes) ---")
    print(b2)

    b3 = re.search(r"else if \(isTrick\) vy = baseSpeed \* 0\.9;\n.*?else if \(isSniper\) vy = 0;", content).group(0)
    print("--- Block 3 (spawn speeds) ---")
    print(b3)

    b4 = re.search(r"else if \(isTrick\) type = 'trick';\n.*?else if \(isSniper\) type = 'sniper';", content).group(0)
    print("--- Block 4 (spawn types) ---")
    print(b4)

    b5 = re.search(r"chanclas.push\({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0,\n.*?sniperTimer: isSniper \? 1\.5 : 0 \}\);", content).group(0)
    print("--- Block 5 (spawn push) ---")
    print(b5)

    b6 = re.search(r"\} else if \(c\.type === 'trick'\) \{[\s\S]*?if \(isa\.anger <= 0\) triggerWin\(\);\n.*?\} else if \(isPerfect\) \{", content).group(0)
    print("--- Block 6 (trySlap ghost) ---")
    print(b6)

    b7 = re.search(r"function drawChancla\(ctx, x, y, w, h, type, rotation\) \{", content).group(0)
    print("--- Block 7 (drawChancla sig) ---")
    print(b7)

    b8 = re.search(r"else if \(type === 'sniper'\) emoji = '🎯';", content).group(0)
    print("--- Block 8 (drawChancla emoji) ---")
    print(b8)

    b9 = re.search(r"for \(const c of chanclas\) drawChancla\(ctx, c\.x, c\.y, c\.w, c\.h, c\.type, c\.rotation\);", content).group(0)
    print("--- Block 9 (drawChanclasAll) ---")
    print(b9)

    b10 = re.search(r"if \(c\.type === 'trick' && !c\.slapped\) \{[\s\S]*?c\.vy = \(dy / mag\) \* 700;\n\s*\}\n\s*\}\n\s*\}", content).group(0)
    print("--- Block 10 (updateChanclas logic) ---")
    print(b10)

    b11 = re.search(r"if \(isa.enraged\) \{[\s\S]*?meteorTimer = 0;\n\s*\}\n\s*\}", content).group(0)
    print("--- Block 11 (meteorTimer) ---")
    print(b11)

    b12 = re.search(r"if \(timeElapsed > 30 && !isa.enraged\) \{\n\s*isa.enraged = true;\n\s*triggerShake\(10, 0\.5\);\n\s*triggerFlash\(0\.3, '#ff4d4d'\);\n\s*playSound\(1000, 0\.3\);\n\s*addFloatText\('¡ENRAGED!', isa\.x, isa\.y - 30\);\n\s*\}", content).group(0)
    print("--- Block 12 (enrage endless) ---")
    print(b12)

    b13 = re.search(r"if \(isa.anger <= isa.maxAnger \* 0\.3 && !isa.enraged\) \{\n\s*isa.enraged = true;\n\s*// Rage phase entry effects\n\s*triggerShake\(10, 0\.5\);\n\s*triggerFlash\(0\.3, '#ff4d4d'\);\n\s*playSound\(1000, 0\.3\);\n\s*addFloatText\('¡ENRAGED!', isa\.x, isa\.y - 30\);\n\s*\}", content).group(0)
    print("--- Block 13 (enrage normal) ---")
    print(b13)

get_blocks('index.html')
# get_blocks('chancla_bomb.html')
