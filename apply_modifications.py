import re

files = ['index.html', 'chancla_bomb.html']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # Step 1
    content = content.replace(
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics' };",
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics', PRESTIGE: 'prestige' };"
    )

    # Step 2
    step2_search = """                if (!gameData.currentHat) gameData.currentHat = 'none';
            } catch (e) { console.error(e); }"""
    step2_replace = """                if (!gameData.currentHat) gameData.currentHat = 'none';
                if (!gameData.prestige) gameData.prestige = 0;
            } catch (e) { console.error(e); }"""
    content = content.replace(step2_search, step2_replace)

    # Step 3
    step3_search = """                ctx.font = '18px sans-serif';
                ctx.fillText('Cosmetics / Cosm.', canvas.width / 2, 590);

                ctx.restore();"""
    step3_replace = """                ctx.font = '18px sans-serif';
                ctx.fillText('Cosmetics / Cosm.', canvas.width / 2, 590);

                if (gameData.stats.wins >= 10) {
                    ctx.fillStyle = '#f44336';
                    roundRect(ctx, 110, 620, canvas.width - 220, 46, 12);
                    ctx.fill();
                    ctx.fillStyle = '#fff';
                    ctx.font = '18px sans-serif';
                    ctx.fillText('Prestige / Prestigio', canvas.width / 2, 650);
                }

                ctx.restore();"""
    content = content.replace(step3_search, step3_replace)

    # Step 4
    step4_search = """                ctx.restore();
            }

            let last = 0;
            function loop(ts) {"""
    step4_replace = """                ctx.restore();
            }

            function drawPrestige() {
                drawBackground();
                drawIsa();
                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('PRESTIGIO / PRESTIGE', canvas.width / 2, 60);
                ctx.font = '16px sans-serif';
                ctx.fillText('Reset wins, coins & upgrades', canvas.width / 2, 120);
                ctx.fillText('for a permanent multiplier!', canvas.width / 2, 140);
                ctx.fillText('Current Prestige: ' + (gameData.prestige || 0), canvas.width / 2, 180);
                const nextMult = (1 + ((gameData.prestige || 0) + 1) * 0.5).toFixed(1);
                ctx.fillStyle = '#ff9f1c';
                ctx.fillText('Next Multiplier: x' + nextMult, canvas.width / 2, 220);

                // Confirm Button
                ctx.fillStyle = '#4caf50';
                roundRect(ctx, 60, 300, canvas.width - 120, 60, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '24px sans-serif';
                ctx.fillText('CONFIRM / CONFIRMAR', canvas.width / 2, 338);

                // Back Button
                ctx.fillStyle = '#e91e63';
                roundRect(ctx, 100, canvas.height - 70, canvas.width - 200, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 40);
                ctx.restore();
            }

            let last = 0;
            function loop(ts) {"""
    content = content.replace(step4_search, step4_replace)

    # Step 4 - loop
    step4b_search = """                else if (state === STATE.COSMETICS) drawCosmetics();
                else if (state === STATE.WIN) {"""
    step4b_replace = """                else if (state === STATE.COSMETICS) drawCosmetics();
                else if (state === STATE.PRESTIGE) drawPrestige();
                else if (state === STATE.WIN) {"""
    content = content.replace(step4b_search, step4b_replace)

    # Step 5 - click
    step5a_search = """                        state = STATE.COSMETICS;
                    }
                } else if (state === STATE.SHOP) {
                    // Check Upgrade Buttons"""
    step5a_replace = """                        state = STATE.COSMETICS;
                    }
                    else if (gameData.stats.wins >= 10 && pos.y >= 620 && pos.y <= 666 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }
                } else if (state === STATE.PRESTIGE) {
                    if (pos.y >= 300 && pos.y <= 360 && pos.x >= 60 && pos.x <= canvas.width - 60) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    } else if (pos.y >= canvas.height - 70 && pos.y <= canvas.height - 24 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                } else if (state === STATE.SHOP) {
                    // Check Upgrade Buttons"""
    content = content.replace(step5a_search, step5a_replace)

    # Step 5 - touch
    step5b_search = """                        state = STATE.COSMETICS;
                    }
                    return;
                }
                if (state === STATE.GAMEOVER || state === STATE.WIN) { resetGame(); return; }"""
    step5b_replace = """                        state = STATE.COSMETICS;
                    }
                    else if (gameData.stats.wins >= 10 && pos.y >= 620 && pos.y <= 666 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }
                    return;
                }
                if (state === STATE.PRESTIGE) {
                    if (pos.y >= 300 && pos.y <= 360 && pos.x >= 60 && pos.x <= canvas.width - 60) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    } else if (pos.y >= canvas.height - 70 && pos.y <= canvas.height - 24 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                    return;
                }
                if (state === STATE.GAMEOVER || state === STATE.WIN) { resetGame(); return; }"""
    content = content.replace(step5b_search, step5b_replace)

    # Step 6 - score and coins
    content = content.replace("score += comboCount;", "score += comboCount * (1 + (gameData.prestige || 0) * 0.5);")
    content = content.replace("score += 20 * c.rallyCount;", "score += 20 * c.rallyCount * (1 + (gameData.prestige || 0) * 0.5);")
    content = content.replace("gameData.coins += 5 * c.rallyCount;", "gameData.coins += Math.floor(5 * c.rallyCount * (1 + (gameData.prestige || 0) * 0.5));")
    content = content.replace("gameData.coins += 2;", "gameData.coins += Math.floor(2 * (1 + (gameData.prestige || 0) * 0.5));")
    content = content.replace("gameData.coins += 1;", "gameData.coins += Math.floor(1 * (1 + (gameData.prestige || 0) * 0.5));")
    content = content.replace("score += 5 + comboCount; // Bonus score for chaotic skill", "score += (5 + comboCount) * (1 + (gameData.prestige || 0) * 0.5); // Bonus score for chaotic skill")
    content = content.replace("score += 5;", "score += 5 * (1 + (gameData.prestige || 0) * 0.5);")
    content = content.replace("score += 1;", "score += 1 * (1 + (gameData.prestige || 0) * 0.5);")
    content = content.replace("gameData.coins += bonus;", "gameData.coins += Math.floor(bonus * (1 + (gameData.prestige || 0) * 0.5));")
    content = content.replace("gameData.coins += earned;", "gameData.coins += Math.floor(earned * (1 + (gameData.prestige || 0) * 0.5));")
    content = content.replace("score += dt * 50; // passive score", "score += dt * 50 * (1 + (gameData.prestige || 0) * 0.5); // passive score")

    with open(file, 'w') as f:
        f.write(content)

    print(f"Modifications applied to {file}")
