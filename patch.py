import re
import sys

def patch_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Add witchTimeTimer initialization
    if 'let witchTimeTimer' not in content:
        content = content.replace('let state = STATE.TITLE;', 'let state = STATE.TITLE;\n            let witchTimeTimer = 0;')

    # 2. Reset witchTimeTimer in resetGame()
    if 'witchTimeTimer = 0;' not in content.split('function resetGame()')[1].split('}')[0]:
        content = content.replace('lastTapRight = 0;', 'lastTapRight = 0;\n                witchTimeTimer = 0;')

    # 3. Add witch time trigger on perfect dodge
    dodge_target = "playSound(850, 0.1);"
    dodge_replace = "playSound(850, 0.1);\n                                witchTimeTimer = 2.0;"
    if 'witchTimeTimer = 2.0;' not in content:
        content = content.replace(dodge_target, dodge_replace)

    # 4. Modify update(dt) to include enemyDt and purple overlay? wait, overlay is in draw()

    with open(filename, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
