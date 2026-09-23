import re

def check_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    b1 = re.search(r"const isSniper.*?Math\.random\(\) < 0\.12;\n\s*const isFire = isa\.enraged.*?Math\.random\(\) < 0\.25;", content)
    b2 = re.search(r"else if \(isTrick\) \{? w = 36; h = 22; \}?\n\s*else if \(isSniper\) \{? w = 34; h = 24; \}?", content)
    b3 = re.search(r"else if \(isTrick\) vy = baseSpeed \* 0\.9;\n\s*else if \(isSniper\) vy = 0;", content)
    b4 = re.search(r"else if \(isTrick\) type = 'trick';\n\s*else if \(isSniper\) type = 'sniper';", content)
    b5 = re.search(r"chanclas\.push\(\{ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0,\n\s*sniperTimer: isSniper \? 1\.5 : 0 \}\);", content)

    b6 = re.search(r"\} else if \(isPerfect\) \{", content)
    b7 = re.search(r"function drawChancla\(ctx, x, y, w, h, type, rotation\) \{", content)
    b8 = re.search(r"else if \(type === 'sniper'\) emoji = '🎯';", content)
    b9 = re.search(r"for \(const c of chanclas\) drawChancla\(ctx, c\.x, c\.y, c\.w, c\.h, c\.type, c\.rotation\);", content)
    b10 = re.search(r"if \(c\.type === 'trick' && !c\.slapped\) \{[\s\S]*?c\.vy = \(dy / mag\) \* 700;\n\s*\}\n\s*\}\n\s*\}", content)

    print(f"--- {filepath} ---")
    for i, b in enumerate([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10]):
        if b:
            print(f"B{i+1} found")
        else:
            print(f"B{i+1} NOT FOUND")

check_file('index.html')
check_file('chancla_bomb.html')
