import re
import sys

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Step 1 modifications
    content = content.replace(
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics', PRESTIGE: 'prestige' };",
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics', PRESTIGE: 'prestige', MISSIONS: 'missions' };"
    )

    content = content.replace(
        "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0, xp: 0, rank: 1 }, achievements: {}, cosmetics: ['none'], currentHat: 'none' };",
        "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0, xp: 0, rank: 1 }, achievements: {}, cosmetics: ['none'], currentHat: 'none', missions: { daily: [], lastDate: '' } };"
    )

    missions_logic = """
            const MISSIONS_LIST = [
                { id: 'slap_10', desc: 'Slap 10 chanclas', type: 'slap', target: 10, reward: 20 },
                { id: 'perfect_5', desc: '5 Perfect Slaps', type: 'perfect', target: 5, reward: 30 },
                { id: 'win_1', desc: 'Win 1 game', type: 'win', target: 1, reward: 50 },
                { id: 'special_2', desc: 'Use Special 2 times', type: 'special', target: 2, reward: 40 },
                { id: 'graze_3', desc: 'Perfect Dodge 3 times', type: 'graze', target: 3, reward: 30 }
            ];

            function checkDailyMissions() {
                const today = new Date().toDateString();
                if (gameData.missions && gameData.missions.lastDate === today) return;
                const shuffled = [...MISSIONS_LIST].sort(() => 0.5 - Math.random());
                gameData.missions = {
                    lastDate: today,
                    daily: shuffled.slice(0, 3).map(m => ({ id: m.id, progress: 0, claimed: false }))
                };
                saveGameData();
            }

            function updateMissionProgress(type, amount) {
                if (!gameData.missions || !gameData.missions.daily) return;
                let updated = false;
                for (let m of gameData.missions.daily) {
                    if (m.claimed) continue;
                    const def = MISSIONS_LIST.find(d => d.id === m.id);
                    if (def && def.type === type && m.progress < def.target) {
                        m.progress = Math.min(def.target, m.progress + amount);
                        updated = true;
                    }
                }
                if (updated) saveGameData();
            }
"""

    content = content.replace(
        "            function saveGameData() {\n                localStorage.setItem('chancla_bomb_save', JSON.stringify(gameData));\n            }",
        "            function saveGameData() {\n                localStorage.setItem('chancla_bomb_save', JSON.stringify(gameData));\n            }\n" + missions_logic
    )

    content = content.replace(
        "checkDailyReward(dt);",
        "checkDailyReward(dt);\n                checkDailyMissions();"
    )

    # Step 2 modifications
    content = content.replace(
        "const panelHeight = (gameData.stats.wins || 1) >= 10 ? 420 : 360;",
        "const panelHeight = (gameData.stats.wins || 1) >= 10 ? 480 : 420;"
    )

    prestige_btn = """                // Prestige Button
                if ((gameData.stats.wins || 1) >= 10) {
                    ctx.fillStyle = '#ffb347';
                    roundRect(ctx, 110, 670, canvas.width - 220, 46, 12);
                    ctx.fill();
                    ctx.fillStyle = '#222';
                    ctx.font = '18px sans-serif';
                    ctx.fillText('Prestige / Prestigio', canvas.width / 2, 700);
                }"""

    new_btns = """                // Missions Button
                ctx.fillStyle = '#4caf50';
                roundRect(ctx, 110, 670, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Misiones / Missions', canvas.width / 2, 700);

                // Prestige Button
                if ((gameData.stats.wins || 1) >= 10) {
                    ctx.fillStyle = '#ffb347';
                    roundRect(ctx, 110, 730, canvas.width - 220, 46, 12);
                    ctx.fill();
                    ctx.fillStyle = '#222';
                    ctx.font = '18px sans-serif';
                    ctx.fillText('Prestige / Prestigio', canvas.width / 2, 760);
                }"""
    content = content.replace(prestige_btn, new_btns)

    # Step 3 modifications
    draw_missions = """            function drawMissions() {
                drawBackground();
                drawIsa();
                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('MISIONES', canvas.width / 2, 80);
                ctx.fillStyle = '#ffd700';
                ctx.font = '24px sans-serif';
                ctx.fillText('💰 ' + gameData.coins, canvas.width / 2, 120);

                let y = 140;
                gameData.missions.daily.forEach(m => {
                    const def = MISSIONS_LIST.find(d => d.id === m.id);
                    if (!def) return;
                    const done = m.progress >= def.target;

                    let bgColor = '#555';
                    if (m.claimed) bgColor = '#4caf50';
                    else if (done) bgColor = '#ff9f1c';

                    ctx.fillStyle = bgColor;
                    roundRect(ctx, 40, y, canvas.width - 80, 70, 10);
                    ctx.fill();
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    roundRect(ctx, 40, y, canvas.width - 80, 70, 10);
                    ctx.stroke();

                    ctx.fillStyle = '#fff';
                    ctx.textAlign = 'left';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillText(def.desc, 55, y + 25);
                    ctx.font = '14px sans-serif';
                    ctx.fillText(`${m.progress} / ${def.target}`, 55, y + 50);

                    ctx.textAlign = 'right';
                    ctx.font = 'bold 14px sans-serif';
                    if (m.claimed) {
                        ctx.fillText('CLAIMED', canvas.width - 55, y + 40);
                    } else if (done) {
                        ctx.fillText('CLAIM 💰 ' + def.reward, canvas.width - 55, y + 40);
                    }
                    y += 85;
                });
                ctx.fillStyle = '#ff5252';
                roundRect(ctx, 100, canvas.height - 80, canvas.width - 200, 50, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 48);
                ctx.restore();
            }

"""
    content = content.replace("            function drawCosmetics() {", draw_missions + "            function drawCosmetics() {")
    content = content.replace("else if (state === STATE.ACHIEVEMENTS) drawAchievements();", "else if (state === STATE.ACHIEVEMENTS) drawAchievements();\n                else if (state === STATE.MISSIONS) drawMissions();")

    btn_checks = """                    // Check Cosmetics Button (110, 560, w, 46)
                    else if (pos.y >= 610 && pos.y <= 656 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                    // Check Prestige Button
                    else if ((gameData.stats.wins || 1) >= 10 && pos.y >= 670 && pos.y <= 716 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }"""

    new_btn_checks = """                    // Check Cosmetics Button (110, 560, w, 46)
                    else if (pos.y >= 610 && pos.y <= 656 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                    // Check Missions Button
                    else if (pos.y >= 670 && pos.y <= 716 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.MISSIONS;
                    }
                    // Check Prestige Button
                    else if ((gameData.stats.wins || 1) >= 10 && pos.y >= 730 && pos.y <= 776 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }"""
    content = content.replace(btn_checks, new_btn_checks)

    touch_btn_checks = """                    else if (pos.y >= 610 && pos.y <= 656 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                    // Check Prestige Button
                    else if ((gameData.stats.wins || 1) >= 10 && pos.y >= 670 && pos.y <= 716 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }"""

    new_touch_btn_checks = """                    else if (pos.y >= 610 && pos.y <= 656 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                    // Check Missions Button
                    else if (pos.y >= 670 && pos.y <= 716 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.MISSIONS;
                    }
                    // Check Prestige Button
                    else if ((gameData.stats.wins || 1) >= 10 && pos.y >= 730 && pos.y <= 776 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }"""
    content = content.replace(touch_btn_checks, new_touch_btn_checks)

    missions_handler = """                } else if (state === STATE.MISSIONS) {
                    let y = 140;
                    for (let m of gameData.missions.daily) {
                        if (pos.y >= y && pos.y <= y + 70 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            const def = MISSIONS_LIST.find(d => d.id === m.id);
                            if (def && m.progress >= def.target && !m.claimed) {
                                m.claimed = true;
                                gameData.coins += def.reward;
                                saveGameData();
                                playSound(1200, 0.1);
                            }
                        }
                        y += 85;
                    }
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 30 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                } else if (state === STATE.COSMETICS) {"""
    content = content.replace("} else if (state === STATE.COSMETICS) {", missions_handler)

    missions_touch_handler = """                if (state === STATE.MISSIONS) {
                    let y = 140;
                    for (let m of gameData.missions.daily) {
                        if (pos.y >= y && pos.y <= y + 70 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            const def = MISSIONS_LIST.find(d => d.id === m.id);
                            if (def && m.progress >= def.target && !m.claimed) {
                                m.claimed = true;
                                gameData.coins += def.reward;
                                saveGameData();
                                playSound(1200, 0.1);
                            }
                        }
                        y += 85;
                    }
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 30 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                }
                if (state === STATE.COSMETICS) {"""
    content = content.replace("if (state === STATE.COSMETICS) {", missions_touch_handler)


    # Step 4 modifications
    content = content.replace(
        "slappedAny = true;",
        "slappedAny = true;\n                            updateMissionProgress('slap', 1);"
    )
    # The above replace will hit twice in trySlap, which is what we want (meteor and normal slap)

    content = content.replace(
        "if (isPerfect) gameData.stats.perfectSlaps++;",
        "if (isPerfect) {\n                            gameData.stats.perfectSlaps++;\n                            updateMissionProgress('perfect', 1);\n                        }"
    )

    content = content.replace(
        "c.grazed = true;",
        "c.grazed = true;\n                                updateMissionProgress('graze', 1);"
    )

    content = content.replace(
        "state = STATE.WIN;",
        "updateMissionProgress('win', 1);\n                state = STATE.WIN;"
    )

    content = content.replace(
        "specialReadyTriggered = false;",
        "specialReadyTriggered = false;\n                    updateMissionProgress('special', 1);"
    )

    with open(filepath, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
