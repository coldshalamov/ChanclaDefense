import re

files = ['index.html', 'chancla_bomb.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Add drawPrestige function before drawCosmetics
    draw_prestige_code = """function drawPrestige() {
                drawBackground();
                drawIsa();
                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('PRESTIGE', canvas.width / 2, 80);

                ctx.font = '18px sans-serif';
                ctx.fillText('Current Prestige: ' + (gameData.prestige || 0), canvas.width / 2, 130);
                ctx.fillText('Multiplier: ' + getPrestigeMult() + 'x', canvas.width / 2, 160);

                ctx.fillText('WARNING: Prestiging resets', canvas.width / 2, 220);
                ctx.fillText('Wins, Coins, and Upgrades!', canvas.width / 2, 250);

                ctx.fillStyle = '#f44336';
                roundRect(ctx, 40, 300, canvas.width - 80, 60, 10);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 24px sans-serif';
                ctx.fillText('PRESTIGE NOW', canvas.width / 2, 340);

                // Back button
                ctx.fillStyle = '#e91e63';
                roundRect(ctx, 40, canvas.height - 70, canvas.width - 80, 50, 10);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '20px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 35);
                ctx.restore();
            }

            function drawCosmetics() {"""
    content = content.replace("function drawCosmetics() {", draw_prestige_code)

    # 2. Add button to title screen
    title_btn_search = "ctx.fillText('Cosmetics / Cosm.', canvas.width / 2, 590);\n\n                ctx.restore();"
    title_btn_replace = """ctx.fillText('Cosmetics / Cosm.', canvas.width / 2, 590);

                if ((gameData.stats.wins || 1) >= 10) {
                    ctx.fillStyle = '#f44336';
                    roundRect(ctx, 110, 620, canvas.width - 220, 46, 12);
                    ctx.fill();
                    ctx.fillStyle = '#fff';
                    ctx.font = '18px sans-serif';
                    ctx.fillText('Prestige / Prestigio', canvas.width / 2, 650);
                }

                ctx.restore();"""
    content = content.replace(title_btn_search, title_btn_replace)

    # 3. Add title click & prestige menu click logic
    click_search = """else if (pos.y >= 560 && pos.y <= 606 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                } else if (state === STATE.SHOP) {"""

    click_replace = """else if (pos.y >= 560 && pos.y <= 606 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                    else if ((gameData.stats.wins || 1) >= 10 && pos.y >= 620 && pos.y <= 666 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }
                } else if (state === STATE.PRESTIGE) {
                    if (pos.y >= 300 && pos.y <= 360 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        playSound(800, 0.1);
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    } else if (pos.y >= canvas.height - 70 && pos.y <= canvas.height - 20) {
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }
                } else if (state === STATE.SHOP) {"""
    content = content.replace(click_search, click_replace)

    # 4. Add to game loop render
    loop_search = """else if (state === STATE.COSMETICS) drawCosmetics();
                else if (state === STATE.WIN)"""
    loop_replace = """else if (state === STATE.COSMETICS) drawCosmetics();
                else if (state === STATE.PRESTIGE) drawPrestige();
                else if (state === STATE.WIN)"""
    content = content.replace(loop_search, loop_replace)

    with open(filename, 'w') as f:
        f.write(content)
