with open("index.html", "r") as f:
    content = f.read()

import re
def get_block(pattern_start, pattern_end):
    start = content.find(pattern_start)
    end = content.find(pattern_end, start) + len(pattern_end)
    return content[start:end]

print("--- TRY SLAP ---")
print(get_block("const comboText = comboPhrase ? ` x${comboCount} ${comboPhrase}` : ` x${comboCount}`;", "if (Math.random() < 0.3) sayRandom('slapSuccess');"))
