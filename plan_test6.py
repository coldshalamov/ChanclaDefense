import re

def main():
    with open('index.html', 'r') as f:
        content = f.read()

    # 1. spawnChancla random logic
    content = content.replace(
        "const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;",
        "const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;\n                const isTrick = !isBomb && !isHoming && !isSuper && !isFire && Math.random() < 0.10;"
    )

    # 2. spawnChancla type logic
    content = content.replace(
        "else if (isHoming) type = 'homing';\n\n                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed });",
        "else if (isHoming) type = 'homing';\n                else if (isTrick) type = 'trick';\n\n                const trickTimer = isTrick ? 0.4 + Math.random() * 0.4 : 0;\n                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 'falling', trickTimer });"
    )

    # 3. drawChancla emoji
    content = content.replace(
        "else if (type === 'homing') emoji = '🪬';",
        "else if (type === 'homing') emoji = '🪬';\n                else if (type === 'trick') emoji = '🃏';"
    )

    # 4. update logic trick
    content = content.replace(
        "// Homing Logic\n                    if (c.type === 'homing' && !c.slapped) {",
        """// Trick Logic
                    if (c.type === 'trick' && !c.slapped) {
                        if (c.trickState === 'falling') {
                            c.trickTimer -= enemyDt;
                            if (c.trickTimer <= 0) {
                                c.trickState = 'paused';
                                c.trickTimer = 0.6; // pause for 0.6s
                                c.vy = 0;
                                c.vx = 0;
                            }
                        } else if (c.trickState === 'paused') {
                            c.trickTimer -= enemyDt;
                            c.x += (Math.random() - 0.5) * 6; // Vibrate effect
                            c.y += (Math.random() - 0.5) * 6;
                            if (c.trickTimer <= 0) {
                                c.trickState = 'darting';
                                const angle = Math.atan2(player.y - c.y, player.x - c.x);
                                const dartSpeed = 700;
                                c.vx = Math.cos(angle) * dartSpeed;
                                c.vy = Math.sin(angle) * dartSpeed;
                            }
                        }
                    }

                    // Homing Logic
                    if (c.type === 'homing' && !c.slapped) {"""
    )

    # 5. trick score bonus
    content = content.replace(
        "const comboText = comboPhrase ? ` x${comboCount} ${comboPhrase}` : ` x${comboCount}`;\n\n                        if (c.rallyCount > 0) {",
        "const comboText = comboPhrase ? ` x${comboCount} ${comboPhrase}` : ` x${comboCount}`;\n\n                        if (c.type === 'trick') {\n                            score += Math.floor(15 * getPrestigeMultiplier());\n                            addFloatText('TRICKED! 🃏', c.x, c.y - 45, '#ff44ff');\n                        }\n\n                        if (c.rallyCount > 0) {"
    )

    # 6. trick boss damage
    content = content.replace(
        "let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);",
        "let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : (c.type === 'trick' ? 10 : 8));"
    )

    with open('index.html', 'w') as f:
        f.write(content)

main()
