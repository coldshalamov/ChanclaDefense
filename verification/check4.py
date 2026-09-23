import re

def get_blocks(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    b1 = re.search(r"const isSniper.*?Math\.random\(\) < 0\.12;\n\s*const isFire = isa\.enraged", content).group(0)
    print("--- Block 1 ---")
    print(b1)

    b2 = re.search(r"else if \(isSniper\) type = 'sniper';", content).group(0)
    print("--- Block 2 ---")
    print(b2)

    b3 = re.search(r"chanclas\.push\(\{ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0,\n\s*sniperTimer: isSniper \? 1\.5 : 0 \}\);", content).group(0)
    print("--- Block 3 ---")
    print(b3)

    b4 = re.search(r"const currentDt = c\.slapped \? dt : enemyDt;\n\s*c\.x \+= c\.vx \* currentDt;\n\s*c\.y \+= c\.vy \* currentDt;\n\s*c\.rotation \+= c\.rotSpeed \* currentDt;", content).group(0)
    print("--- Block 4 ---")
    print(b4)

    b5 = re.search(r"function drawChancla\(ctx, x, y, w, h, type, rotation\) \{\n\s*ctx\.save\(\);\n\s*ctx\.translate\(x, y\);", content).group(0)
    print("--- Block 5 ---")
    print(b5)

    b6 = re.search(r"else if \(type === 'sniper'\) emoji = '🎯';", content).group(0)
    print("--- Block 6 ---")
    print(b6)

    b7 = re.search(r"for \(const c of chanclas\) drawChancla\(ctx, c\.x, c\.y, c\.w, c\.h, c\.type, c\.rotation\);", content).group(0)
    print("--- Block 7 ---")
    print(b7)

    b8 = re.search(r"else if \(c\.type === 'trick'\) \{[\s\S]*?if \(isa\.anger <= 0\) triggerWin\(\);\n\s*\} else if \(isPerfect\) \{", content).group(0)
    print("--- Block 8 ---")
    print(b8)

get_blocks('index.html')
