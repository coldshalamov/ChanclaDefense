import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Click listener
    old_click = """                if (state === STATE.TITLE) {
                    // Check Play Button (110, 380, w, 46)
                    if (pos.y >= 380 && pos.y <= 426 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        startGameFromTitle();
                    }
                    // Check Shop Button (110, 450, w, 46)
                    else if (pos.y >= 450 && pos.y <= 496 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.SHOP;
                    }
                } else if (state === STATE.SHOP) {"""

    new_click = """                if (state === STATE.TITLE) {
                    // Check Play Button (110, 395, w, 46)
                    if (pos.y >= 395 && pos.y <= 441 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        startGameFromTitle();
                    }
                    // Check Shop Button (110, 455, w, 46)
                    else if (pos.y >= 455 && pos.y <= 501 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.SHOP;
                    }
                    // Check Stats Button (110, 515, w, 46)
                    else if (pos.y >= 515 && pos.y <= 561 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.STATS;
                    }
                } else if (state === STATE.STATS) {
                    // Check Back Button
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                    }
                } else if (state === STATE.SHOP) {"""

    content = content.replace(old_click, new_click, 1)

    # Touch listener
    old_touch = """                if (state === STATE.TITLE) {
                    if (pos.y >= 380 && pos.y <= 426) startGameFromTitle();
                    else if (pos.y >= 450 && pos.y <= 496) state = STATE.SHOP;
                    return;
                }
                if (state === STATE.GAMEOVER || state === STATE.WIN) { resetGame(); return; }"""

    new_touch = """                if (state === STATE.TITLE) {
                    if (pos.y >= 395 && pos.y <= 441) startGameFromTitle();
                    else if (pos.y >= 455 && pos.y <= 501) state = STATE.SHOP;
                    else if (pos.y >= 515 && pos.y <= 561) state = STATE.STATS;
                    return;
                }
                if (state === STATE.STATS) {
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50) state = STATE.TITLE;
                    return;
                }
                if (state === STATE.GAMEOVER || state === STATE.WIN) { resetGame(); return; }"""

    content = content.replace(old_touch, new_touch, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Patched event listeners successfully.")
