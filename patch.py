import re

def patch_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Init gameData
    init_str = """                if (!gameData.stats.rank) gameData.stats.rank = 1;
                if (gameData.stats.maxCombo === undefined) gameData.stats.maxCombo = 0;"""
    replacement_init = """                if (!gameData.stats.rank) gameData.stats.rank = 1;
                if (gameData.stats.maxCombo === undefined) gameData.stats.maxCombo = 0;
                if (gameData.prestigeTokens === undefined) gameData.prestigeTokens = 0;
                if (!gameData.prestigeUpgrades) gameData.prestigeUpgrades = { golden_chance: 0, witch_time: 0, combo_shield: 0 };"""
    content = content.replace(init_str, replacement_init)

    # 2. Golden chance in spawnChancla
    spawn_str = """            function spawnChancla() {
                const isBomb = Math.random() < 0.08;
                const isGolden = !isBomb && Math.random() < 0.05;"""
    replacement_spawn = """            function spawnChancla() {
                const extraGolden = (gameData.prestigeUpgrades?.golden_chance || 0) * 0.02;
                const isBomb = Math.random() < 0.08;
                const isGolden = !isBomb && Math.random() < (0.05 + extraGolden);"""
    content = content.replace(spawn_str, replacement_spawn)

    # 3. Combo shield in trySlap
    combo_str = """                        score += Math.floor(comboCount * getPrestigeMultiplier());

                        // Increase special attack bar"""
    replacement_combo = """                        score += Math.floor(comboCount * getPrestigeMultiplier());

                        if (gameData.prestigeUpgrades?.combo_shield && comboCount % 30 === 0 && comboCount > 0) {
                            if (!player.shield) {
                                player.shield = true;
                                addFloatText('COMBO SHIELD! 🛡️', player.x, player.y - 50, '#9bfffa');
                                playSound(1200, 0.2);
                            }
                        }

                        // Increase special attack bar"""
    content = content.replace(combo_str, replacement_combo)

    # 4. Witch time in updateChanclas
    witch_str = """                                playSound(850, 0.1);
                                witchTimeTimer = 2.0;
                                triggerFlash(0.2, '#cc00ff');"""
    replacement_witch = """                                playSound(850, 0.1);
                                const extraWitchTime = (gameData.prestigeUpgrades?.witch_time || 0) * 0.5;
                                witchTimeTimer = 2.0 + extraWitchTime;
                                triggerFlash(0.2, '#cc00ff');"""
    content = content.replace(witch_str, replacement_witch)

    # 5. drawPrestige
    draw_prestige_str = """            function drawPrestige() {
                drawBackground();
                drawIsa(); // Background decoration

                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('PRESTIGE', canvas.width / 2, 80);

                ctx.font = '16px sans-serif';
                ctx.fillStyle = '#ddd';
                wrapText(ctx, "Reset your wins, coins, and upgrades to gain a permanent +50% multiplier to score and coins!", canvas.width / 2, 130, canvas.width - 60, 22);

                ctx.fillStyle = '#ffd700';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText(`Current Prestige: ${gameData.prestige || 0}`, canvas.width / 2, 200);

                ctx.fillStyle = '#4caf50';
                ctx.fillText(`Next Multiplier: x${(1 + ((gameData.prestige || 0) + 1) * 0.5).toFixed(1)}`, canvas.width / 2, 240);

                // Warning
                ctx.fillStyle = '#ff5252';
                ctx.font = 'bold 16px sans-serif';
                ctx.fillText('WARNING: THIS CANNOT BE UNDONE!', canvas.width / 2, 300);

                // Prestige Confirmation Button
                ctx.fillStyle = '#ffb347';
                roundRect(ctx, 60, 400, canvas.width - 120, 60, 12);
                ctx.fill();
                ctx.fillStyle = '#111';
                ctx.font = 'bold 24px sans-serif';
                ctx.fillText('PRESTIGE NOW', canvas.width / 2, 438);

                // Back Button
                ctx.fillStyle = '#ff5252';
                roundRect(ctx, 100, canvas.height - 70, canvas.width - 200, 50, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 38);

                ctx.restore();
            }"""

    replacement_draw_prestige = """            function drawPrestige() {
                drawBackground();
                drawIsa();

                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('PRESTIGE SHOP', canvas.width / 2, 50);

                ctx.font = '14px sans-serif';
                ctx.fillStyle = '#ddd';
                wrapText(ctx, "Reset your wins, coins, and upgrades for +50% multiplier and 1 Prestige Token!", canvas.width / 2, 80, canvas.width - 40, 20);

                ctx.fillStyle = '#ffd700';
                ctx.font = 'bold 18px sans-serif';
                ctx.fillText(`Tokens: ${gameData.prestigeTokens || 0} | Mult: x${(1 + (gameData.prestige || 0) * 0.5).toFixed(1)}`, canvas.width / 2, 130);

                let y = 150;
                const prestigeUpgradesList = [
                    { id: 'golden_chance', name: 'Golden Touch', icon: '✨', cost: 1, maxLevel: 3, desc: '+2% Golden Chancla chance' },
                    { id: 'witch_time', name: 'Time Wizard', icon: '⏳', cost: 1, maxLevel: 3, desc: '+0.5s Witch Time' },
                    { id: 'combo_shield', name: 'Combo Shield', icon: '🛡️', cost: 2, maxLevel: 1, desc: 'Shield at 30 combo' }
                ];

                prestigeUpgradesList.forEach(u => {
                    const level = (gameData.prestigeUpgrades || {})[u.id] || 0;
                    const isMax = level >= u.maxLevel;
                    const affordable = (gameData.prestigeTokens || 0) >= u.cost;

                    ctx.fillStyle = isMax ? '#4caf50' : (affordable ? '#9c27b0' : '#555');
                    roundRect(ctx, 30, y, canvas.width - 60, 60, 10);
                    ctx.fill();
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    roundRect(ctx, 30, y, canvas.width - 60, 60, 10);
                    ctx.stroke();

                    ctx.font = '24px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#fff';
                    ctx.fillText(u.icon, 45, y + 38);

                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillText(`${u.name} (${level}/${u.maxLevel})`, 80, y + 25);

                    ctx.font = '12px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(u.desc, 80, y + 45);

                    ctx.textAlign = 'right';
                    ctx.font = 'bold 14px sans-serif';
                    if (isMax) {
                        ctx.fillStyle = '#fff';
                        ctx.fillText('MAX', canvas.width - 45, y + 35);
                    } else {
                        ctx.fillStyle = affordable ? '#ffd700' : '#ff9999';
                        ctx.fillText(`🪙 ${u.cost}`, canvas.width - 45, y + 35);
                    }
                    y += 70;
                });

                // Prestige Confirmation Button
                ctx.fillStyle = '#ffb347';
                roundRect(ctx, 50, 390, canvas.width - 100, 50, 12);
                ctx.fill();
                ctx.fillStyle = '#111';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('PRESTIGE NOW', canvas.width / 2, 422);

                ctx.fillStyle = '#ff5252';
                ctx.font = 'bold 12px sans-serif';
                ctx.fillText('WARNING: CANNOT BE UNDONE!', canvas.width / 2, 460);

                // Back Button
                ctx.fillStyle = '#ff5252';
                roundRect(ctx, 100, canvas.height - 60, canvas.width - 200, 40, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 18px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 34);

                ctx.restore();
            }"""
    content = content.replace(draw_prestige_str, replacement_draw_prestige)

    # 6. Click handler
    click_str = """                } else if (state === STATE.PRESTIGE) {
                    // Check Prestige Confirmation (60, 400, w-120, 60)
                    if (pos.y >= 400 && pos.y <= 460 && pos.x >= 60 && pos.x <= canvas.width - 60) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        playSound(1200, 0.4);
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                    // Check Back Button (100, canvas.height - 70, w-200, 50)
                    else if (pos.y >= canvas.height - 70 && pos.y <= canvas.height - 20 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }"""

    replacement_click = """                } else if (state === STATE.PRESTIGE) {
                    const prestigeUpgradesList = [
                        { id: 'golden_chance', cost: 1, maxLevel: 3 },
                        { id: 'witch_time', cost: 1, maxLevel: 3 },
                        { id: 'combo_shield', cost: 2, maxLevel: 1 }
                    ];
                    let y = 150;
                    for (let u of prestigeUpgradesList) {
                        if (pos.y >= y && pos.y <= y + 60 && pos.x >= 30 && pos.x <= canvas.width - 30) {
                            if (!gameData.prestigeUpgrades) gameData.prestigeUpgrades = { golden_chance: 0, witch_time: 0, combo_shield: 0 };
                            const level = gameData.prestigeUpgrades[u.id] || 0;
                            if (level < u.maxLevel && (gameData.prestigeTokens || 0) >= u.cost) {
                                gameData.prestigeTokens -= u.cost;
                                gameData.prestigeUpgrades[u.id] = level + 1;
                                saveGameData();
                                playSound(1200, 0.1);
                            } else {
                                playSound(200, 0.1);
                            }
                        }
                        y += 70;
                    }

                    // Check Prestige Confirmation (50, 390, w-100, 50)
                    if (pos.y >= 390 && pos.y <= 440 && pos.x >= 50 && pos.x <= canvas.width - 50) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.prestigeTokens = (gameData.prestigeTokens || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        playSound(1200, 0.4);
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                    // Check Back Button (100, canvas.height - 60, w-200, 40)
                    else if (pos.y >= canvas.height - 60 && pos.y <= canvas.height - 20 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }"""
    content = content.replace(click_str, replacement_click)

    # 7. Touch handler
    touch_str = """                if (state === STATE.PRESTIGE) {
                    // Check Prestige Confirmation (60, 400, w-120, 60)
                    if (pos.y >= 400 && pos.y <= 460 && pos.x >= 60 && pos.x <= canvas.width - 60) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        playSound(1200, 0.4);
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                    // Check Back Button (100, canvas.height - 70, w-200, 50)
                    else if (pos.y >= canvas.height - 70 && pos.y <= canvas.height - 20 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                    return;
                }"""

    replacement_touch = """                if (state === STATE.PRESTIGE) {
                    const prestigeUpgradesList = [
                        { id: 'golden_chance', cost: 1, maxLevel: 3 },
                        { id: 'witch_time', cost: 1, maxLevel: 3 },
                        { id: 'combo_shield', cost: 2, maxLevel: 1 }
                    ];
                    let y = 150;
                    for (let u of prestigeUpgradesList) {
                        if (pos.y >= y && pos.y <= y + 60 && pos.x >= 30 && pos.x <= canvas.width - 30) {
                            if (!gameData.prestigeUpgrades) gameData.prestigeUpgrades = { golden_chance: 0, witch_time: 0, combo_shield: 0 };
                            const level = gameData.prestigeUpgrades[u.id] || 0;
                            if (level < u.maxLevel && (gameData.prestigeTokens || 0) >= u.cost) {
                                gameData.prestigeTokens -= u.cost;
                                gameData.prestigeUpgrades[u.id] = level + 1;
                                saveGameData();
                                playSound(1200, 0.1);
                            } else {
                                playSound(200, 0.1);
                            }
                        }
                        y += 70;
                    }

                    // Check Prestige Confirmation (50, 390, w-100, 50)
                    if (pos.y >= 390 && pos.y <= 440 && pos.x >= 50 && pos.x <= canvas.width - 50) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.prestigeTokens = (gameData.prestigeTokens || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        playSound(1200, 0.4);
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                    // Check Back Button (100, canvas.height - 60, w-200, 40)
                    else if (pos.y >= canvas.height - 60 && pos.y <= canvas.height - 20 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                    return;
                }"""
    content = content.replace(touch_str, replacement_touch)

    with open(filename, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
