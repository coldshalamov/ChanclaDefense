import re

def get_blocks(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    b12 = re.search(r"if \(timeElapsed > 30 && !isa.enraged\) \{\n\s*isa.enraged = true;\n\s*triggerShake\(10, 0\.5\);\n\s*triggerFlash\(0\.3, '#ff4d4d'\);\n\s*playSound\(1000, 0\.3\);\n\s*addFloatText\('¡ENRAGED!', isa\.x, isa\.y - 30\);\n\s*\}", content).group(0)
    print("--- Block 12 (enrage endless) ---")
    print(b12)

    b13 = re.search(r"if \(isa.anger <= isa.maxAnger \* 0\.3 && !isa.enraged\) \{\n\s*isa.enraged = true;\n\s*// Rage phase entry effects\n\s*triggerShake\(10, 0\.5\);\n\s*triggerFlash\(0\.3, '#ff4d4d'\);\n\s*playSound\(1000, 0\.3\);\n\s*addFloatText\('¡ENRAGED!', isa\.x, isa\.y - 30\);\n\s*\}", content).group(0)
    print("--- Block 13 (enrage normal) ---")
    print(b13)

get_blocks('index.html')
