import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update loop to handle ACHIEVEMENTS state
    content = content.replace(
        "else if (state === STATE.SHOP) drawShop();",
        "else if (state === STATE.SHOP) drawShop();\n                else if (state === STATE.ACHIEVEMENTS) drawAchievements();"
    )

    # 2. Add Touch scroll variables
    content = content.replace(
        "const touch = { left: false, right: false };",
        "const touch = { left: false, right: false };\n            let touchStartY = 0;\n            let lastTouchY = 0;"
    )

    # 3. Add Achievements interaction to canvas.addEventListener('click')
    click_logic = """
                } else if (state === STATE.ACHIEVEMENTS) {
                    let y = 150 + achScrollY;
                    ACH_DATA.forEach((ach) => {
                        const progress = gameData.stats[ach.type] || 0;
                        const isCompleted = progress >= ach.target;
                        const isClaimed = gameData.achievements[ach.id];

                        if (pos.y >= y && pos.y <= y + 90 && pos.x >= 30 && pos.x <= canvas.width - 30) {
                            if (isCompleted && !isClaimed) {
                                gameData.achievements[ach.id] = true;
                                gameData.coins += ach.reward;
                                gameData.stats.totalCoinsEarned += ach.reward;
                                saveGameData();
                                playSound(1200, 0.2); // Claim sound
                            }
                        }
                        y += 105;
                    });

                    // Back Button
                    if (pos.y >= canvas.height - 90 && pos.y <= canvas.height - 40 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                        achScrollY = 0;
                    }
"""
    content = content.replace(
        "} else if (state === STATE.GAMEOVER || state === STATE.WIN) {",
        click_logic + "\n                } else if (state === STATE.GAMEOVER || state === STATE.WIN) {"
    )

    # 4. Add title screen button logic for achievements (Click)
    content = content.replace(
        "else if (pos.y >= 450 && pos.y <= 496 && pos.x >= 110 && pos.x <= canvas.width - 110) {\n                        state = STATE.SHOP;\n                    }",
        "else if (pos.y >= 450 && pos.y <= 496 && pos.x >= 110 && pos.x <= canvas.width - 110) {\n                        state = STATE.SHOP;\n                    }\n                    // Check Achievements Button (110, 520, w, 46)\n                    else if (pos.y >= 520 && pos.y <= 566 && pos.x >= 110 && pos.x <= canvas.width - 110) {\n                        state = STATE.ACHIEVEMENTS;\n                        achScrollY = 0;\n                    }"
    )

    # 5. Add Achievements interaction to canvas.addEventListener('touchstart')
    touch_logic = """
                if (state === STATE.ACHIEVEMENTS) {
                    touchStartY = pos.y;
                    lastTouchY = pos.y;
                    return;
                }
"""
    content = content.replace(
        "if (state === STATE.TITLE) {",
        touch_logic + "\n                if (state === STATE.TITLE) {"
    )

    # 6. Title screen touch targets update
    content = content.replace(
        "else if (pos.y >= 450 && pos.y <= 496) state = STATE.SHOP;",
        "else if (pos.y >= 450 && pos.y <= 496) state = STATE.SHOP;\n                    else if (pos.y >= 520 && pos.y <= 566) { state = STATE.ACHIEVEMENTS; achScrollY = 0; }"
    )

    # 7. Add touchend/touchmove logic for achievements scrolling/clicking
    scroll_logic = """
            canvas.addEventListener('touchmove', (e) => {
                if (state === STATE.ACHIEVEMENTS) {
                    const touchPoint = e.touches[0];
                    const rect = canvas.getBoundingClientRect();
                    const scaleY = canvas.height / rect.height;
                    const pos = { y: (touchPoint.clientY - rect.top) * scaleY };

                    achScrollY += (pos.y - lastTouchY);
                    lastTouchY = pos.y;

                    // Constrain scroll
                    const maxScroll = Math.min(0, canvas.height - 240 - (ACH_DATA.length * 105));
                    achScrollY = Math.max(maxScroll, Math.min(0, achScrollY));
                    e.preventDefault(); // prevent pull-to-refresh
                }
            }, { passive: false });

            canvas.addEventListener('touchend', (e) => {
                touch.left = false;
                touch.right = false;

                if (state === STATE.ACHIEVEMENTS) {
                    // It was a tap if we barely moved
                    if (Math.abs(lastTouchY - touchStartY) < 10) {
                        const pos = lastTouchY; // use last known Y
                        const touchPoint = e.changedTouches[0];
                        const rect = canvas.getBoundingClientRect();
                        const scaleX = canvas.width / rect.width;
                        const posX = (touchPoint.clientX - rect.left) * scaleX;

                        let y = 150 + achScrollY;
                        ACH_DATA.forEach((ach) => {
                            const progress = gameData.stats[ach.type] || 0;
                            const isCompleted = progress >= ach.target;
                            const isClaimed = gameData.achievements[ach.id];

                            if (pos >= y && pos <= y + 90 && posX >= 30 && posX <= canvas.width - 30) {
                                if (isCompleted && !isClaimed) {
                                    gameData.achievements[ach.id] = true;
                                    gameData.coins += ach.reward;
                                    gameData.stats.totalCoinsEarned += ach.reward;
                                    saveGameData();
                                    playSound(1200, 0.2); // Claim sound
                                }
                            }
                            y += 105;
                        });

                        // Back Button
                        if (pos >= canvas.height - 90 && pos <= canvas.height - 40 && posX >= 100 && posX <= canvas.width - 100) {
                            state = STATE.TITLE;
                            achScrollY = 0;
                        }
                    }
                }
            });
"""
    content = content.replace(
        "canvas.addEventListener('touchend', () => { touch.left = false; touch.right = false; });",
        scroll_logic
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('index.html')
patch_file('chancla_bomb.html')
