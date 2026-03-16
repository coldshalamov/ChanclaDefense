import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    ach_screen_code = """
            let achScrollY = 0;
            function drawAchievements() {
                drawBackground();
                drawIsa(); // Background decoration

                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('ACHIEVEMENTS', canvas.width / 2, 80);

                ctx.fillStyle = '#ffd700';
                ctx.font = '24px sans-serif';
                ctx.fillText('💰 ' + gameData.coins, canvas.width / 2, 120);

                // Define a clipping region for scrolling area
                ctx.beginPath();
                ctx.rect(0, 140, canvas.width, canvas.height - 240);
                ctx.clip();

                let y = 150 + achScrollY;
                ACH_DATA.forEach((ach, index) => {
                    const progress = gameData.stats[ach.type] || 0;
                    const isCompleted = progress >= ach.target;
                    const isClaimed = gameData.achievements[ach.id];

                    // Card Background
                    let bgColor = '#444';
                    let borderColor = '#888';

                    if (isClaimed) {
                        bgColor = '#2e5a2e'; // Dark green
                        borderColor = '#4caf50';
                    } else if (isCompleted) {
                        bgColor = '#b26500'; // Dark orange
                        borderColor = '#ff9800';
                    }

                    ctx.fillStyle = bgColor;
                    roundRect(ctx, 30, y, canvas.width - 60, 90, 10);
                    ctx.fill();

                    // Border
                    ctx.strokeStyle = borderColor;
                    ctx.lineWidth = 2;
                    roundRect(ctx, 30, y, canvas.width - 60, 90, 10);
                    ctx.stroke();

                    // Title
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#fff';
                    ctx.font = 'bold 18px sans-serif';
                    ctx.fillText(ach.name, 45, y + 25);

                    // Desc
                    ctx.font = '14px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(ach.desc, 45, y + 45);

                    // Progress Bar
                    const barWidth = 150;
                    const barHeight = 10;
                    const pValue = Math.min(1, progress / ach.target);
                    ctx.fillStyle = '#222';
                    roundRect(ctx, 45, y + 60, barWidth, barHeight, 5);
                    ctx.fill();

                    if (pValue > 0) {
                        ctx.fillStyle = isCompleted ? '#4caf50' : '#2196f3';
                        ctx.save();
                        ctx.beginPath();
                        roundRect(ctx, 45, y + 60, barWidth * pValue, barHeight, 5);
                        ctx.clip();
                        roundRect(ctx, 45, y + 60, barWidth * pValue, barHeight, 5);
                        ctx.fill();
                        ctx.restore();
                    }

                    ctx.textAlign = 'right';
                    ctx.font = '12px sans-serif';
                    ctx.fillStyle = '#ccc';
                    ctx.fillText(`${Math.floor(Math.min(progress, ach.target))}/${ach.target}`, 45 + barWidth, y + 55);

                    // Reward / Claim
                    ctx.textAlign = 'center';
                    if (isClaimed) {
                        ctx.fillStyle = '#4caf50';
                        ctx.font = 'bold 16px sans-serif';
                        ctx.fillText('✅ CLAIMED', canvas.width - 80, y + 45);
                    } else if (isCompleted) {
                        ctx.fillStyle = '#fff';
                        ctx.font = 'bold 14px sans-serif';
                        ctx.fillText('TAP TO CLAIM', canvas.width - 80, y + 40);
                        ctx.fillStyle = '#ffd700';
                        ctx.font = 'bold 18px sans-serif';
                        ctx.fillText('💰 ' + ach.reward, canvas.width - 80, y + 65);
                    } else {
                        ctx.fillStyle = '#ffd700';
                        ctx.font = '18px sans-serif';
                        ctx.fillText('💰 ' + ach.reward, canvas.width - 80, y + 55);
                    }

                    y += 105;
                });

                ctx.restore(); // Remove clip

                // Scroll hints (if list is long)
                if (y - achScrollY > canvas.height - 240) {
                    ctx.fillStyle = '#aaa';
                    ctx.textAlign = 'center';
                    ctx.font = '12px sans-serif';
                    ctx.fillText('↕️ Scroll to see more ↕️', canvas.width / 2, canvas.height - 110);
                }

                // Back Button
                ctx.fillStyle = '#ff5252';
                roundRect(ctx, 100, canvas.height - 90, canvas.width - 200, 50, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 58);
            }
"""
    content = content.replace(
        "function drawTitleScreen() {",
        ach_screen_code + "\n            function drawTitleScreen() {"
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('index.html')
patch_file('chancla_bomb.html')
