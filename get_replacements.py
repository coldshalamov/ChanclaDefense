import re

with open('index.html', 'r') as f:
    content = f.read()

def print_block(regex, name):
    print(f"\n--- {name} ---")
    match = re.search(regex, content, re.DOTALL)
    if match:
        print(match.group(0))
    else:
        print("Not found")

print_block(r'const STATE = \{[^}]+\};', 'STATE')
print_block(r'if \(!gameData\.currentHat\) gameData\.currentHat = \'none\';', 'gameData init')
print_block(r'function drawTitleScreen\(\) \{.*?(?=function)', 'drawTitle')
print_block(r'score \+= comboCount;', 'score1')
print_block(r'gameData\.coins \+= bonus;', 'coins bonus')
print_block(r'if \(state === STATE\.TITLE\) \{[^{}]*startGameFromTitle[^{}]*SHOP[^{}]*\}', 'click title')
