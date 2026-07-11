with open("index.html", "r") as f:
    content = f.read()

def get_block(start_str, end_str):
    start = content.find(start_str)
    end = content.find(end_str, start)
    if start != -1 and end != -1:
        return content[start:end]
    return ""

print("--- spawnChancla ---")
print(get_block("function spawnChancla()", "function addFloatText"))
print("--- updateChanclas ---")
print(get_block("function updateChanclas(dt)", "function drawFloatTexts()"))
print("--- drawChancla ---")
print(get_block("function drawChancla(ctx, x, y, w, h, type, rotation)", "function drawDialogue()"))
print("--- drawChanclasAll ---")
print(get_block("function drawChanclasAll()", "function drawWinScreen()"))
print("--- trySlap ---")
print(get_block("function trySlap()", "function fireSpecialAttack()"))
