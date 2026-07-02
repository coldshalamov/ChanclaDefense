import re

files = ['index.html', 'chancla_bomb.html']

draw_prestige = """            function drawPrestige() {
                drawBackground();
                drawIsa();

                ctx.save();
                ctx.fillStyle = 'rgba(0,0,0,0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#ffb347';
                ctx.textAlign = 'center';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText('PRESTIGE', canvas.width / 2, 100);

                ctx.fillStyle = '#fff';
                ctx.font = '16px sans-serif';
                ctx.fillText('Reset wins, coins, and upgrades', canvas.width / 2, 160);
                ctx.fillText('for a permanent +0.5x multiplier!', canvas.width / 2, 190);

                ctx.fillStyle = '#ff9f1c';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('Current Prestige: ' + (gameData.prestige || 0), canvas.width / 2, 250);
                ctx.fillText('Next Multiplier: ' + ((1 + ((gameData.prestige || 0) + 1) * 0.5).toFixed(1)) + 'x', canvas.width / 2, 280);

                // Prestige Button
                ctx.fillStyle = '#4caf50';
                roundRect(ctx, 40, 350, canvas.width - 80, 70, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 24px sans-serif';
                ctx.fillText('DO PRESTIGE!', canvas.width / 2, 395);

                // Back Button
                ctx.fillStyle = '#f44336';
                roundRect(ctx, 100, canvas.height - 100, canvas.width - 200, 50, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 68);

                ctx.restore();
            }

            function drawCosmetics() {"""

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # Insert drawPrestige before drawCosmetics
    content = content.replace("            function drawCosmetics() {", draw_prestige)

    # Update loop
    content = content.replace("else if (state === STATE.COSMETICS) drawCosmetics();", "else if (state === STATE.COSMETICS) drawCosmetics();\n                else if (state === STATE.PRESTIGE) drawPrestige();")

    with open(filename, 'w') as f:
        f.write(content)

print("Step 4 done")
