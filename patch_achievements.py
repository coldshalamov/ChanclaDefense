import os

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add ACHIEVEMENTS to STATE
    content = content.replace(
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop' };",
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements' };"
    )

    # 2. Add gameData.achievements initialization
    content = content.replace(
        "if (!gameData.stats) gameData.stats = { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 };",
        "if (!gameData.stats) gameData.stats = { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 };\n                if (!gameData.achievements) gameData.achievements = {};"
    )

    # 3. Add drawAchievements function
    draw_achievements = """
            function drawAchievements() {
                drawBackground();
                drawIsa(); // Background decoration

                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 28px sans-serif';
                ctx.fillText('LOGROS / ACHIEVEMENTS', canvas.width / 2, 80);

                ctx.fillStyle = '#ffd700';
                ctx.font = '20px sans-serif';
                ctx.fillText('💰 ' + gameData.coins, canvas.width / 2, 115);

                const achList = [
                    { id: 'first_blood', name: 'First Slap', desc: 'Slap 1 chancla', icon: '✋', goal: 1, current: gameData.stats.totalSlaps, reward: 10 },
                    { id: 'slap_master', name: 'Slap Master', desc: 'Slap 100 chanclas', icon: '🔥', goal: 100, current: gameData.stats.totalSlaps, reward: 50 },
                    { id: 'perfect_timing', name: 'Perfect Timing', desc: '10 Perfect Slaps', icon: '✨', goal: 10, current: gameData.stats.perfectSlaps, reward: 25 },
                    { id: 'high_roller', name: 'High Roller', desc: 'Reach Score 500', icon: '💯', goal: 500, current: gameData.bestScore, reward: 100 },
                    { id: 'rich_gringo', name: 'Rich Gringo', desc: 'Earn 500 Coins', icon: '💎', goal: 500, current: gameData.stats.totalCoinsEarned, reward: 100 },
                    { id: 'veteran', name: 'Veteran', desc: 'Play 50 Games', icon: '🎮', goal: 50, current: gameData.stats.gamesPlayed, reward: 75 }
                ];

                let y = 140;
                achList.forEach(a => {
                    const claimed = gameData.achievements[a.id];
                    const progress = Math.min(a.current, a.goal);
                    const canClaim = progress >= a.goal && !claimed;

                    // Button bg
                    ctx.fillStyle = claimed ? '#4caf50' : (canClaim ? '#ff9f1c' : '#555');
                    roundRect(ctx, 30, y, canvas.width - 60, 75, 10);
                    ctx.fill();

                    // Border
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    roundRect(ctx, 30, y, canvas.width - 60, 75, 10);
                    ctx.stroke();

                    // Icon
                    ctx.font = '28px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#fff';
                    ctx.fillText(a.icon, 45, y + 48);

                    // Text
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillText(a.name, 85, y + 28);
                    ctx.font = '12px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(a.desc, 85, y + 45);
                    ctx.fillStyle = '#aaa';
                    ctx.fillText(`${progress}/${a.goal}`, 85, y + 62);

                    // Status / Reward
                    ctx.textAlign = 'right';
                    ctx.font = 'bold 14px sans-serif';
                    if (claimed) {
                        ctx.fillStyle = '#fff';
                        ctx.fillText('CLAIMED', canvas.width - 45, y + 42);
                    } else if (canClaim) {
                        ctx.fillStyle = '#fff';
                        ctx.fillText('CLAIM!', canvas.width - 45, y + 35);
                        ctx.fillStyle = '#ffd700';
                        ctx.fillText(`+${a.reward} 💰`, canvas.width - 45, y + 55);
                    } else {
                        ctx.fillStyle = '#ffd700';
                        ctx.fillText(`Reward: ${a.reward}`, canvas.width - 45, y + 42);
                    }

                    y += 85;
                });

                // Back Button
                ctx.fillStyle = '#ff5252';
                roundRect(ctx, 100, canvas.height - 65, canvas.width - 200, 45, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 18px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 38);

                ctx.restore();
            }
"""
    content = content.replace("function drawTitleScreen() {", draw_achievements + "\n            function drawTitleScreen() {")

    # 4. Add Achievements button to Title Screen
    old_title_screen = """                // Shop Button
                ctx.fillStyle = '#2196f3';
                roundRect(ctx, 110, 450, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Shop / Tienda', canvas.width / 2, 480);

                ctx.restore();"""
    new_title_screen = """                // Shop Button
                ctx.fillStyle = '#2196f3';
                roundRect(ctx, 110, 440, canvas.width - 220, 40, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '16px sans-serif';
                ctx.fillText('Shop / Tienda', canvas.width / 2, 466);

                // Achievements Button
                ctx.fillStyle = '#9b59b6';
                roundRect(ctx, 110, 495, canvas.width - 220, 40, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '16px sans-serif';
                ctx.fillText('Logros / Achiev.', canvas.width / 2, 521);

                ctx.restore();"""
    content = content.replace(old_title_screen, new_title_screen)

    # Also adjust the background rect of Title Screen
    content = content.replace(
        "roundRect(ctx, 30, 260, canvas.width - 60, 200, 16);",
        "roundRect(ctx, 30, 260, canvas.width - 60, 290, 16);"
    )


    # 5. Handle draw loop
    content = content.replace(
        "else if (state === STATE.SHOP) drawShop();",
        "else if (state === STATE.SHOP) drawShop();\n                else if (state === STATE.ACHIEVEMENTS) drawAchievements();"
    )

    # 6. Click handler
    old_click_title = """                    // Check Shop Button (110, 450, w, 46)
                    else if (pos.y >= 450 && pos.y <= 496 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.SHOP;
                    }"""
    new_click_title = """                    // Check Shop Button
                    else if (pos.y >= 440 && pos.y <= 480 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.SHOP;
                    }
                    // Check Achievements Button
                    else if (pos.y >= 495 && pos.y <= 535 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.ACHIEVEMENTS;
                        setDirectionsVisible(false);
                    }"""
    content = content.replace(old_click_title, new_click_title)

    # 7. Click handler for achievements
    click_achievements = """                } else if (state === STATE.ACHIEVEMENTS) {
                    const achList = [
                        { id: 'first_blood', goal: 1, current: gameData.stats.totalSlaps, reward: 10 },
                        { id: 'slap_master', goal: 100, current: gameData.stats.totalSlaps, reward: 50 },
                        { id: 'perfect_timing', goal: 10, current: gameData.stats.perfectSlaps, reward: 25 },
                        { id: 'high_roller', goal: 500, current: gameData.bestScore, reward: 100 },
                        { id: 'rich_gringo', goal: 500, current: gameData.stats.totalCoinsEarned, reward: 100 },
                        { id: 'veteran', goal: 50, current: gameData.stats.gamesPlayed, reward: 75 }
                    ];
                    let y = 140;
                    for (let a of achList) {
                        if (pos.y >= y && pos.y <= y + 75 && pos.x >= 30 && pos.x <= canvas.width - 30) {
                            if (!gameData.achievements[a.id] && a.current >= a.goal) {
                                gameData.achievements[a.id] = true;
                                gameData.coins += a.reward;
                                saveGameData();
                                playSound(1200, 0.1);
                            }
                        }
                        y += 85;
                    }
                    if (pos.y >= canvas.height - 65 && pos.y <= canvas.height - 20 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                } else if (state === STATE.GAMEOVER || state === STATE.WIN) {"""
    content = content.replace("                } else if (state === STATE.GAMEOVER || state === STATE.WIN) {", click_achievements)

    # 8. Touch handler
    old_touch_title = """                if (state === STATE.TITLE) {
                    if (pos.y >= 380 && pos.y <= 426) startGameFromTitle();
                    else if (pos.y >= 450 && pos.y <= 496) state = STATE.SHOP;
                    return;
                }"""
    new_touch_title = """                if (state === STATE.TITLE) {
                    if (pos.y >= 380 && pos.y <= 426) startGameFromTitle();
                    else if (pos.y >= 440 && pos.y <= 480) state = STATE.SHOP;
                    else if (pos.y >= 495 && pos.y <= 535) {
                        state = STATE.ACHIEVEMENTS;
                        setDirectionsVisible(false);
                    }
                    return;
                }"""
    content = content.replace(old_touch_title, new_touch_title)

    # 9. Touch handler for achievements
    touch_achievements = """                    // Check Back Button
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50) {
                        state = STATE.TITLE;
                    }
                    return;
                }

                if (state === STATE.ACHIEVEMENTS) {
                    const achList = [
                        { id: 'first_blood', goal: 1, current: gameData.stats.totalSlaps, reward: 10 },
                        { id: 'slap_master', goal: 100, current: gameData.stats.totalSlaps, reward: 50 },
                        { id: 'perfect_timing', goal: 10, current: gameData.stats.perfectSlaps, reward: 25 },
                        { id: 'high_roller', goal: 500, current: gameData.bestScore, reward: 100 },
                        { id: 'rich_gringo', goal: 500, current: gameData.stats.totalCoinsEarned, reward: 100 },
                        { id: 'veteran', goal: 50, current: gameData.stats.gamesPlayed, reward: 75 }
                    ];
                    let y = 140;
                    for (let a of achList) {
                        if (pos.y >= y && pos.y <= y + 75 && pos.x >= 30 && pos.x <= canvas.width - 30) {
                            if (!gameData.achievements[a.id] && a.current >= a.goal) {
                                gameData.achievements[a.id] = true;
                                gameData.coins += a.reward;
                                saveGameData();
                                playSound(1200, 0.1);
                            }
                        }
                        y += 85;
                    }
                    if (pos.y >= canvas.height - 65 && pos.y <= canvas.height - 20 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                    return;
                }

                if (state === STATE.PLAYING) {"""
    content = content.replace("""                    // Check Back Button
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50) {
                        state = STATE.TITLE;
                    }
                    return;
                }

                if (state === STATE.PLAYING) {""", touch_achievements)


    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
