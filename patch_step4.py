import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_loop = """                if (state === STATE.TITLE) drawTitleScreen();
                else if (state === STATE.SHOP) drawShop();
                else if (state === STATE.WIN) {"""
    new_loop = """                if (state === STATE.TITLE) drawTitleScreen();
                else if (state === STATE.SHOP) drawShop();
                else if (state === STATE.ACHIEVEMENTS) drawAchievements();
                else if (state === STATE.WIN) {"""

    if old_loop in content:
        content = content.replace(old_loop, new_loop, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('chancla_bomb.html')
