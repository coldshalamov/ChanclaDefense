with open("index.html", "r") as f:
    content = f.read()

import re
def get_block(pattern_start, pattern_end):
    start = content.find(pattern_start)
    end = content.find(pattern_end, start) + len(pattern_end)
    return content[start:end]

print("--- SPAWN CHANCLA ---")
print(get_block("const isBomb = Math.random() < 0.08;", "if (isSuper) sayPlayer('super');"))

print("\n--- TRY SLAP ---")
print(get_block("const comboText = comboPhrase ? ` x${comboCount} ${comboPhrase}` : ` x${comboCount}`;", "if (isPerfect) {"))

print("\n--- UPDATE CHANCLAS ---")
print(get_block("if (c.type === 'bomb') damage = 20;", "damage += (gameData.upgrades.power || 0) * 2;"))

print("\n--- DRAW CHANCLA ---")
print(get_block("else if (type === 'homing') emoji = '🪬';", "// Prioritize Noto Color Emoji"))
