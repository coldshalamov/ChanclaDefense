
import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. CSS Patch
# Find .touch-zone { ... pointer-events: auto; } and change to none
# Then add .game-playing .touch-zone { pointer-events: auto; }
# The regex needs to be robust against whitespace
css_pattern = r"(\.touch-zone\s*\{[^}]*pointer-events:\s*)auto(\s*;[^}]*\})"
replacement = r"\1none\2\n        body.game-playing .touch-zone { pointer-events: auto; }"

new_content = re.sub(css_pattern, replacement, content)

if new_content == content:
    print("CSS patch failed to match pattern.")
    # Debug print
    import re
    m = re.search(r"\.touch-zone\s*\{", content)
    if m:
        print("Found .touch-zone start")
else:
    print("CSS patch applied.")

# 2. JS Patch
# resetGame: add class
if "body.classList.add('game-playing')" not in new_content:
    new_content = new_content.replace(
        "state = STATE.PLAYING;",
        "state = STATE.PLAYING; body.classList.add('game-playing');"
    )
    print("Patched resetGame")

# endGame: remove class
if "body.classList.remove('game-playing')" not in new_content:
    new_content = new_content.replace(
        "state = STATE.GAMEOVER;",
        "state = STATE.GAMEOVER; body.classList.remove('game-playing');"
    )
    print("Patched endGame")

# WIN state
# Found in updateChanclas and updateSpecialProjectiles
if "state = STATE.WIN;" in new_content:
    new_content = new_content.replace(
        "state = STATE.WIN;",
        "state = STATE.WIN; body.classList.remove('game-playing');"
    )
    print("Patched WIN state")

with open('index.html', 'w') as f:
    f.write(new_content)
print("Saved index.html")
