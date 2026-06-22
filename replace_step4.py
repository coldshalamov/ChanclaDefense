import os

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replacements
    target1 = """                drawPlayerDialogue();
            }"""
    replacement1 = """                drawPlayerDialogue();
            }

            function drawPrestigeScreen() {
                drawBackground();
                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#ffeb3b';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('PRESTIGE', canvas.width / 2, 100);

                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Reset Wins, Coins, and Upgrades.', canvas.width / 2, 150);
                ctx.fillText('Keep Cosmetics and Achievements.', canvas.width / 2, 180);

                ctx.fillStyle = '#00e5ff';
                ctx.font = '22px sans-serif';
                ctx.fillText('Current Prestige: ' + (gameData.prestige || 0), canvas.width / 2, 230);
                ctx.fillText('Bonus Multiplier: ' + (1 + (gameData.prestige || 0) * 0.5) + 'x', canvas.width / 2, 260);

                // Prestige Now Button
                ctx.fillStyle = '#e91e63';
                roundRect(ctx, 40, 320, canvas.width - 80, 60, 10);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 24px sans-serif';
                ctx.fillText('Prestige Now (+0.5x)', canvas.width / 2, 358);

                // Back Button
                ctx.fillStyle = '#555';
                roundRect(ctx, 100, canvas.height - 70, canvas.width - 200, 50, 10);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 38);

                ctx.restore();
            }"""

    target2 = """                else if (state === STATE.ACHIEVEMENTS) drawAchievements();
                else if (state === STATE.COSMETICS) drawCosmetics();
                else if (state === STATE.WIN) {"""
    replacement2 = """                else if (state === STATE.ACHIEVEMENTS) drawAchievements();
                else if (state === STATE.COSMETICS) drawCosmetics();
                else if (state === STATE.PRESTIGE) drawPrestigeScreen();
                else if (state === STATE.WIN) {"""

    target3 = """                    // Check Back Button
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 30 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                }"""
    replacement3 = """                    // Check Back Button
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 30 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                } else if (state === STATE.PRESTIGE) {
                    if (pos.y >= 320 && pos.y <= 380 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        playSound(1200, 0.1);
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                    if (pos.y >= canvas.height - 70 && pos.y <= canvas.height - 20 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                }"""

    if target1 in content:
        content = content.replace(target1, replacement1)
    else:
        print(f"Failed to find target1 in {filepath}")

    if target2 in content:
        content = content.replace(target2, replacement2)
    else:
        print(f"Failed to find target2 in {filepath}")

    if target3 in content:
        content = content.replace(target3, replacement3)
    else:
        print(f"Failed to find target3 in {filepath}")

    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file("index.html")
replace_in_file("chancla_bomb.html")
