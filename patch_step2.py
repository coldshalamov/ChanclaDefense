import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    helper_func = """
            function getUnclaimedAchievementsCount() {
                let count = 0;
                ACH_DATA.forEach(ach => {
                    const progress = gameData.stats[ach.type] || 0;
                    const isCompleted = progress >= ach.target;
                    const isClaimed = gameData.achievements[ach.id];
                    if (isCompleted && !isClaimed) count++;
                });
                return count;
            }
"""
    content = content.replace(
        "function drawTitleScreen() {",
        helper_func + "\n            function drawTitleScreen() {"
    )

    ach_button_code = """
                // Achievements Button
                ctx.fillStyle = '#9c27b0';
                roundRect(ctx, 110, 520, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Achievements', canvas.width / 2, 550);

                const unclaimedCount = getUnclaimedAchievementsCount();
                if (unclaimedCount > 0) {
                    ctx.fillStyle = '#f44336';
                    ctx.beginPath();
                    ctx.arc(canvas.width - 100, 520, 12, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    ctx.fillStyle = '#fff';
                    ctx.font = 'bold 12px sans-serif';
                    ctx.fillText(unclaimedCount, canvas.width - 100, 524);
                }
"""

    # We need to increase the size of the background box of the title screen to fit the extra button.
    content = content.replace(
        "roundRect(ctx, 30, 260, canvas.width - 60, 200, 16);",
        "roundRect(ctx, 30, 260, canvas.width - 60, 270, 16);"
    )

    content = content.replace(
        "ctx.fillText('Shop / Tienda', canvas.width / 2, 480);",
        "ctx.fillText('Shop / Tienda', canvas.width / 2, 480);\n\n" + ach_button_code
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('index.html')
patch_file('chancla_bomb.html')
