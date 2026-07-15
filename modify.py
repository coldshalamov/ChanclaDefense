import re

files = ["index.html", "chancla_bomb.html"]
for f in files:
    with open(f, 'r') as file:
        content = file.read()

    # 1. Add golden to spawnChancla
    content = re.sub(
        r"(const isFire = isa\.enraged && !isBomb && !isHoming && !isSuper && Math\.random\(\) < 0\.25;)",
        r"\1\n                const isGolden = !isBomb && !isHoming && !isSuper && !isFire && Math.random() < 0.05;",
        content
    )

    content = re.sub(
        r"(else if \(isHoming\) \{ w = 36; h = 36; \})",
        r"\1\n                else if (isGolden) { w = 36; h = 20; }",
        content
    )

    content = re.sub(
        r"(else if \(isHoming\) vy = baseSpeed \* 0\.8; // slightly slower vertical speed)",
        r"\1\n                else if (isGolden) vy = baseSpeed * 1.2;",
        content
    )

    content = re.sub(
        r"(else if \(isHoming\) type = 'homing';)",
        r"\1\n                else if (isGolden) type = 'golden';",
        content
    )

    # 2. Add golden emoji
    content = re.sub(
        r"(else if \(type === 'homing'\) emoji = '🪬';)",
        r"\1\n                else if (type === 'golden') emoji = '✨🩴';",
        content
    )

    # 3. Add shadow for golden
    content = re.sub(
        r"(\} else if \(type === 'homing'\) \{\s*ctx\.shadowColor = '#8a2be2';\s*ctx\.shadowBlur = 15;\s*\})",
        r"\1 else if (type === 'golden') {\n                        ctx.shadowColor = '#ffd700';\n                        ctx.shadowBlur = 15;\n                    }",
        content
    )

    # 4. trySlap logic
    golden_slap_code = """
                        if (c.type === 'golden') {
                            score += Math.floor(500 * getPrestigeMultiplier());
                            gameData.coins += Math.floor(25 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(25 * getPrestigeMultiplier());
                            triggerFlash(0.3, '#ffd700');
                            addFloatText('GOLDEN SLAP! ✨', c.x, c.y - 30, '#ffd700', 18);
                            playSound(900, 0.3);

                            // Reflect all other active chanclas directly at the boss
                            for (let j = 0; j < chanclas.length; j++) {
                                const other = chanclas[j];
                                if (!other.slapped && other !== c && other.type !== 'meteor') {
                                    other.slapped = true;
                                    other.vx = (isa.x - other.x) * 1.5;
                                    other.vy = -600;
                                }
                            }
                        }

                        if (Math.random() < 0.3) sayRandom('slapSuccess');"""
    content = content.replace("if (Math.random() < 0.3) sayRandom('slapSuccess');", golden_slap_code.strip())

    # 5. updateChanclas damage
    content = re.sub(
        r"(if \(c\.type === 'bomb'\) damage = 20;)",
        r"\1\n                            if (c.type === 'golden') damage = 35;",
        content
    )

    with open(f, 'w') as file:
        file.write(content)
