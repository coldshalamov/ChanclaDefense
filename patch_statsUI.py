import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update STATE constant
    old_state = "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop' };"
    new_state = "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', STATS: 'stats' };"
    content = content.replace(old_state, new_state, 1)

    # 2. Add drawStats function
    draw_stats_func = """            function drawStats() {
                drawBackground();
                drawIsa(); // Background decoration

                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('STATS / INFO', canvas.width / 2, 80);

                ctx.fillStyle = '#ffd700';
                ctx.font = '24px sans-serif';
                ctx.fillText('Lifetime Statistics', canvas.width / 2, 120);

                const statsData = [
                    { label: 'Games Played:', value: gameData.stats.gamesPlayed, icon: '🎮' },
                    { label: 'Total Slaps:', value: gameData.stats.totalSlaps, icon: '✋' },
                    { label: 'Perfect Slaps:', value: gameData.stats.perfectSlaps, icon: '✨' },
                    { label: 'Total Coins:', value: gameData.stats.totalCoinsEarned, icon: '💰' }
                ];

                let y = 180;
                statsData.forEach(s => {
                    // Box
                    ctx.fillStyle = '#2196f3';
                    roundRect(ctx, 40, y, canvas.width - 80, 60, 10);
                    ctx.fill();

                    // Border
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    roundRect(ctx, 40, y, canvas.width - 80, 60, 10);
                    ctx.stroke();

                    // Icon
                    ctx.font = '24px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#fff';
                    ctx.fillText(s.icon, 55, y + 38);

                    // Label
                    ctx.font = 'bold 18px sans-serif';
                    ctx.fillText(s.label, 95, y + 36);

                    // Value
                    ctx.textAlign = 'right';
                    ctx.font = 'bold 20px sans-serif';
                    ctx.fillStyle = '#ffd700';
                    ctx.fillText(s.value.toString(), canvas.width - 55, y + 38);

                    y += 80;
                });

                // Back Button
                ctx.fillStyle = '#ff5252';
                roundRect(ctx, 100, canvas.height - 100, canvas.width - 200, 50, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 68);

                ctx.restore();
            }

            function drawTitleScreen()"""

    content = content.replace("            function drawTitleScreen()", draw_stats_func, 1)

    # 3. Update drawTitleScreen to include Best Score / Coins and Stats Button
    old_title_screen = """                // Shop Button
                ctx.fillStyle = '#2196f3';
                roundRect(ctx, 110, 450, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Shop / Tienda', canvas.width / 2, 480);

                ctx.restore();"""

    new_title_screen = """                // Text below title
                ctx.fillStyle = '#ffd700';
                ctx.font = '16px sans-serif';
                ctx.fillText('Best Score: ' + gameData.bestScore + ' | 💰 ' + gameData.coins, canvas.width / 2, 320);

                // Readjust instructions text
                ctx.fillStyle = '#fff';
                ctx.font = '14px sans-serif';
                ctx.fillText('¡Manotea (Espacio) las chanclas para regresarlas!', canvas.width / 2, 350);

                // Play Button
                ctx.fillStyle = '#ff9f1c';
                roundRect(ctx, 110, 380, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#222';
                ctx.font = '18px sans-serif';
                ctx.fillText('Jugar / Play', canvas.width / 2, 410);

                // Shop Button
                ctx.fillStyle = '#2196f3';
                roundRect(ctx, 110, 450, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Shop / Tienda', canvas.width / 2, 480);

                // Stats Button
                ctx.fillStyle = '#9c27b0';
                roundRect(ctx, 110, 520, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Stats / Info', canvas.width / 2, 550);

                ctx.restore();"""

    # This replacement is a bit trickier, let's just replace the whole drawTitleScreen tail.

    old_full_title = """            function drawTitleScreen() {
                drawBackground();
                drawIsa();
                drawPlayer();
                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                roundRect(ctx, 30, 260, canvas.width - 60, 200, 16);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = '24px sans-serif';
                ctx.fillText('Chancla Bomb', canvas.width / 2, 300);
                ctx.font = '16px sans-serif';
                ctx.fillText('Isa vs. Su Gringo Para Siempre', canvas.width / 2, 330);
                ctx.font = '14px sans-serif';
                ctx.fillText('¡Manotea (Espacio) las chanclas para regresarlas!', canvas.width / 2, 360);

                // Play Button
                ctx.fillStyle = '#ff9f1c';
                roundRect(ctx, 110, 380, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#222';
                ctx.font = '18px sans-serif';
                ctx.fillText('Jugar / Play', canvas.width / 2, 410);

                // Shop Button
                ctx.fillStyle = '#2196f3';
                roundRect(ctx, 110, 450, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Shop / Tienda', canvas.width / 2, 480);

                ctx.restore();
            }"""

    new_full_title = """            function drawTitleScreen() {
                drawBackground();
                drawIsa();
                drawPlayer();
                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                roundRect(ctx, 30, 260, canvas.width - 60, 240, 16); // Increased height to fit more text
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = '24px sans-serif';
                ctx.fillText('Chancla Bomb', canvas.width / 2, 300);

                // Text below title
                ctx.fillStyle = '#ffd700';
                ctx.font = '16px sans-serif';
                ctx.fillText('Best Score: ' + gameData.bestScore + ' | 💰 ' + gameData.coins, canvas.width / 2, 325);

                ctx.fillStyle = '#fff';
                ctx.font = '16px sans-serif';
                ctx.fillText('Isa vs. Su Gringo Para Siempre', canvas.width / 2, 350);
                ctx.font = '14px sans-serif';
                ctx.fillText('¡Manotea (Espacio) las chanclas para regresarlas!', canvas.width / 2, 375);

                // Play Button
                ctx.fillStyle = '#ff9f1c';
                roundRect(ctx, 110, 395, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#222';
                ctx.font = '18px sans-serif';
                ctx.fillText('Jugar / Play', canvas.width / 2, 425);

                // Shop Button
                ctx.fillStyle = '#2196f3';
                roundRect(ctx, 110, 455, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Shop / Tienda', canvas.width / 2, 485);

                // Stats Button
                ctx.fillStyle = '#9c27b0';
                roundRect(ctx, 110, 515, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Stats / Info', canvas.width / 2, 545);

                ctx.restore();
            }"""
    content = content.replace(old_full_title, new_full_title, 1)

    # 4. Update the loop switch/if else chain
    old_loop = """                if (state === STATE.PLAYING || state === STATE.WIN) update(dt);
                if (state === STATE.TITLE) drawTitleScreen();
                else if (state === STATE.SHOP) drawShop();"""

    new_loop = """                if (state === STATE.PLAYING || state === STATE.WIN) update(dt);
                if (state === STATE.TITLE) drawTitleScreen();
                else if (state === STATE.SHOP) drawShop();
                else if (state === STATE.STATS) drawStats();"""
    content = content.replace(old_loop, new_loop, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Patched UI and state logic successfully.")
