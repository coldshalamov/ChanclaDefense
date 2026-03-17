import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_func = """
            function drawAchievements() {
                drawBackground();
                drawIsa(); // Background decoration

                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 30px sans-serif';
                ctx.fillText('LOGROS / MEDALS', canvas.width / 2, 70);

                ctx.fillStyle = '#ffd700';
                ctx.font = '22px sans-serif';
                ctx.fillText('💰 ' + gameData.coins, canvas.width / 2, 100);

                const medals = [
                    { id: 'slaps_100', name: 'Slap Happy', icon: '✋', target: 100, current: gameData.stats.totalSlaps, reward: 50, desc: 'Slap 100 chanclas' },
                    { id: 'score_50', name: 'Gringo Pro', icon: '🏆', target: 50, current: gameData.bestScore, reward: 100, desc: 'Reach 50 score' },
                    { id: 'games_20', name: 'Addicted', icon: '🕹️', target: 20, current: gameData.stats.gamesPlayed, reward: 75, desc: 'Play 20 games' },
                    { id: 'perfect_50', name: 'Perfecto!', icon: '✨', target: 50, current: gameData.stats.perfectSlaps, reward: 150, desc: '50 Perfect Slaps' }
                ];

                let y = 130;
                medals.forEach(m => {
                    const claimed = gameData.achievements[m.id];
                    const progress = Math.min(1, m.current / m.target);
                    const completed = progress >= 1;

                    // Button bg
                    ctx.fillStyle = claimed ? '#4caf50' : (completed ? '#ff9f1c' : '#333');
                    roundRect(ctx, 30, y, canvas.width - 60, 80, 10);
                    ctx.fill();

                    // Border
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    roundRect(ctx, 30, y, canvas.width - 60, 80, 10);
                    ctx.stroke();

                    // Icon
                    ctx.font = '30px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#fff';
                    ctx.fillText(m.icon, 45, y + 50);

                    // Text
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillText(m.name, 85, y + 30);
                    ctx.font = '13px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(m.desc, 85, y + 50);

                    // Progress / Status
                    if (!claimed && !completed) {
                        // Progress bar
                        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                        roundRect(ctx, 85, y + 60, 150, 8, 4);
                        ctx.fill();
                        ctx.fillStyle = '#2196f3';
                        roundRect(ctx, 85, y + 60, 150 * progress, 8, 4);
                        ctx.fill();
                        ctx.fillStyle = '#fff';
                        ctx.textAlign = 'right';
                        ctx.font = '12px sans-serif';
                        ctx.fillText(`${m.current}/${m.target}`, canvas.width - 45, y + 68);
                    } else if (completed && !claimed) {
                        ctx.fillStyle = '#fff';
                        ctx.textAlign = 'right';
                        ctx.font = 'bold 16px sans-serif';
                        ctx.fillText('CLAIM 💰' + m.reward, canvas.width - 45, y + 45);
                    } else {
                        ctx.fillStyle = '#fff';
                        ctx.textAlign = 'right';
                        ctx.font = 'bold 16px sans-serif';
                        ctx.fillText('CLAIMED ✔️', canvas.width - 45, y + 45);
                    }

                    y += 95;
                });

                // Back Button
                ctx.fillStyle = '#ff5252';
                roundRect(ctx, 100, canvas.height - 80, canvas.width - 200, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 50);

                ctx.restore();
            }

            function drawTitleScreen()"""

    if "function drawTitleScreen()" in content:
        content = content.replace("function drawTitleScreen()", new_func, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('chancla_bomb.html')
