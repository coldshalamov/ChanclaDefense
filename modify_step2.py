import re

files = ['index.html', 'chancla_bomb.html']

prestige_btn = """                if (gameData.stats.wins >= 10) {
                    ctx.fillStyle = '#ffb347';
                    roundRect(ctx, 110, 620, canvas.width - 220, 46, 12);
                    ctx.fill();
                    ctx.fillStyle = '#fff';
                    ctx.font = '18px sans-serif';
                    ctx.fillText('Prestige / Prestigio', canvas.width / 2, 650);
                }

                ctx.restore();
            }"""

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # 4. Prestige Button on Title Screen
    content = content.replace("                ctx.restore();\n            }\n\n            function drawGameOver()", prestige_btn + "\n\n            function drawGameOver()")

    with open(filename, 'w') as f:
        f.write(content)

print("Step 2 done")
