import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Patch 1: Add touchstart logic for Achievements button on Title screen
    old_title_touch = """                if (state === STATE.TITLE) {
                    if (pos.y >= 380 && pos.y <= 426) startGameFromTitle();
                    else if (pos.y >= 450 && pos.y <= 496) state = STATE.SHOP;
                    return;
                }"""
    new_title_touch = """                if (state === STATE.TITLE) {
                    if (pos.y >= 380 && pos.y <= 426) startGameFromTitle();
                    else if (pos.y >= 450 && pos.y <= 496) state = STATE.SHOP;
                    else if (pos.y >= 520 && pos.y <= 566) state = STATE.ACHIEVEMENTS;
                    return;
                }"""
    if old_title_touch in content:
        content = content.replace(old_title_touch, new_title_touch, 1)

    # Patch 2: Add touchstart logic for Achievements state
    old_ach_touch = """                    // Check Back Button
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50) {
                        state = STATE.TITLE;
                    }
                    return;
                }

                if (state === STATE.PLAYING) {"""
    new_ach_touch = """                    // Check Back Button
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50) {
                        state = STATE.TITLE;
                    }
                    return;
                }

                if (state === STATE.ACHIEVEMENTS) {
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
                                playSound(1200, 0.1);
                            } else if (!claimed) {
                                playSound(200, 0.1); // Error
                            }
                        }
                        y += 95;
                    }
                    // Check Back Button
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 34) {
                        state = STATE.TITLE;
                    }
                    return;
                }

                if (state === STATE.PLAYING) {"""
    if old_ach_touch in content:
        content = content.replace(old_ach_touch, new_ach_touch, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('chancla_bomb.html')
