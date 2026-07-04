import re

with open('index.html', 'r') as f:
    content = f.read()

print("STATE definition:")
state_match = re.search(r'const STATE = \{[^}]+\};', content)
if state_match:
    print(state_match.group(0))

print("\ngameData initialization:")
gamedata_match = re.search(r'let gameData = \{[^}]+\};', content)
if gamedata_match:
    print(gamedata_match.group(0))

print("\nCoins in trySlap:")
tryslap_match = re.search(r'function trySlap\(x, y\).*?gameData\.stats\.totalSlaps\+\+;', content, re.DOTALL)
if tryslap_match:
    print(tryslap_match.group(0)[:500])
