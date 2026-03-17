import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Patch 1: Add click listener logic for Achievements button on Title screen
    old_title_clicks = """                    // Check Shop Button (110, 450, w, 46)
                    else if (pos.y >= 450 && pos.y <= 496 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.SHOP;
                    }
                } else if (state === STATE.SHOP) {"""
    new_title_clicks = """                    // Check Shop Button (110, 450, w, 46)
                    else if (pos.y >= 450 && pos.y <= 496 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.SHOP;
                    }
                    // Check Achievements Button (110, 520, w, 46)
                    else if (pos.y >= 520 && pos.y <= 566 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.ACHIEVEMENTS;
                    }
                } else if (state === STATE.SHOP) {"""
    if old_title_clicks in content:
        content = content.replace(old_title_clicks, new_title_clicks, 1)

    # Patch 2: Add click listener logic for Achievements state
    old_ach_clicks = """                    // Check Back Button
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                    }
                } else if (state === STATE.GAMEOVER || state === STATE.WIN) {"""
    new_ach_clicks = """                    // Check Back Button
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                    }
                } else if (state === STATE.ACHIEVEMENTS) {
                    const medals = [
                        { id: 'slaps_100', target: 100, current: gameData.stats.totalSlaps, reward: 50 },
                        { id: 'score_50', target: 50, current: gameData.bestScore, reward: 100 },
                        { id: 'games_20', target: 20, current: gameData.stats.gamesPlayed, reward: 75 },
                        { id: 'perfect_50', target: 50, current: gameData.stats.perfectSlaps, reward: 150 }
                    ];
                    let y = 130;
                    for (let m of medals) {
                        if (pos.y >= y && pos.y <= y + 80 && pos.x >= 30 && pos.x <= canvas.width - 30) {
                            const claimed = gameData.achievements[m.id];
                            const progress = Math.min(1, m.current / m.target);
                            const completed = progress >= 1;
                            if (completed && !claimed) {
                                gameData.coins += m.reward;
                                gameData.achievements[m.id] = true;
                                saveGameData();
                                playSound(1200, 0.1); // Cha-ching!
                            } else if (!claimed) {
                                playSound(200, 0.1); // Error
                            }
                        }
                        y += 95;
                    }
                    // Check Back Button
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 34 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                    }
                } else if (state === STATE.GAMEOVER || state === STATE.WIN) {"""
    if old_ach_clicks in content:
        content = content.replace(old_ach_clicks, new_ach_clicks, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('chancla_bomb.html')
