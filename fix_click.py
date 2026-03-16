import sys

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The issue: In step 4 we replaced "if (state === STATE.TITLE) {" with touch_logic + "\n                if (state === STATE.TITLE) {"
    # But this string appears in both canvas.addEventListener('click', ...) and canvas.addEventListener('touchstart', ...)
    # Let's fix the click listener by removing the injected touch_logic.

    # We want to remove:
    # "if (state === STATE.ACHIEVEMENTS) {\n                    touchStartY = pos.y;\n                    lastTouchY = pos.y;\n                    return;\n                }"
    # But only from the click handler. The easiest way is to find the click listener block and replace it.

    # Actually, we can just replace the whole first occurrence of that block, because the first occurrence is in the click listener.

    bad_block = """                if (state === STATE.ACHIEVEMENTS) {
                    touchStartY = pos.y;
                    lastTouchY = pos.y;
                    return;
                }

                if (state === STATE.TITLE) {"""

    good_block = "                if (state === STATE.TITLE) {"

    # Replace ONLY the first occurrence (which is inside the 'click' listener)
    content = content.replace(bad_block, good_block, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")

fix_file('index.html')
fix_file('chancla_bomb.html')
