import os

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replacements
    target1 = """                ctx.fillText('Cosmetics / Cosm.', canvas.width / 2, 590);

                ctx.restore();
            }"""
    replacement1 = """                ctx.fillText('Cosmetics / Cosm.', canvas.width / 2, 590);

                if ((gameData.stats.wins || 1) >= 10) {
                    ctx.fillStyle = '#ffeb3b';
                    roundRect(ctx, 110, 620, canvas.width - 220, 46, 12);
                    ctx.fill();
                    ctx.fillStyle = '#000';
                    ctx.font = '18px sans-serif';
                    ctx.fillText('Prestige / Prestigio', canvas.width / 2, 650);
                }

                ctx.restore();
            }"""

    target2 = """                    // Check Cosmetics Button (110, 560, w, 46)
                    else if (pos.y >= 560 && pos.y <= 606 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                } else if (state === STATE.SHOP) {"""
    replacement2 = """                    // Check Cosmetics Button (110, 560, w, 46)
                    else if (pos.y >= 560 && pos.y <= 606 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                    // Check Prestige Button (110, 620, w, 46)
                    else if ((gameData.stats.wins || 1) >= 10 && pos.y >= 620 && pos.y <= 666 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }
                } else if (state === STATE.SHOP) {"""

    if target1 in content:
        content = content.replace(target1, replacement1)
    else:
        print(f"Failed to find target1 in {filepath}")

    if target2 in content:
        content = content.replace(target2, replacement2)
    else:
        print(f"Failed to find target2 in {filepath}")

    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file("index.html")
replace_in_file("chancla_bomb.html")
