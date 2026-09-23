import re

def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update isFire and add isGhost
    content = re.sub(
        r"(const isSniper.*?Math\.random\(\) < 0\.12;)\n\s*const isFire = isa\.enraged",
        r"\1\n                const isGhost = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && Math.random() < 0.15;\n                const isFire = isa.enraged && !isGhost",
        content
    )

    # 2. Spawn size
    content = re.sub(
        r"(else if \(isSniper\) \{? w = 34; h = 24; \}?)",
        r"\1\n                else if (isGhost) { w = 34; h = 20; }",
        content
    )

    # 3. Spawn vy
    content = re.sub(
        r"(else if \(isSniper\) vy = 0;)",
        r"\1\n                else if (isGhost) vy = baseSpeed * 1.1;",
        content
    )

    # 4. Spawn type
    content = re.sub(
        r"(else if \(isSniper\) type = 'sniper';)",
        r"\1\n                else if (isGhost) type = 'ghost';",
        content
    )

    # 5. Push to chanclas (adding invisible: false)
    content = re.sub(
        r"(chanclas\.push\(\{ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0,\n\s*sniperTimer: isSniper \? 1\.5 : 0) (\}\);)",
        r"\1, invisible: false \2",
        content
    )

    # 6. Ghost Logic in updateChanclas
    ghost_logic = r"""const currentDt = c.slapped ? dt : enemyDt;
                    if (c.type === 'ghost' && !c.slapped) {
                        if (c.y > canvas.height * 0.25 && c.y < canvas.height * 0.75) {
                            c.invisible = true;
                        } else {
                            c.invisible = false;
                        }
                    }
                    c.x += c.vx * currentDt;
                    c.y += c.vy * currentDt;
                    c.rotation += c.rotSpeed * currentDt;"""

    content = re.sub(
        r"const currentDt = c\.slapped \? dt : enemyDt;\n\s*c\.x \+= c\.vx \* currentDt;\n\s*c\.y \+= c\.vy \* currentDt;\n\s*c\.rotation \+= c\.rotSpeed \* currentDt;",
        ghost_logic,
        content
    )

    # 7. drawChancla signature
    content = re.sub(
        r"function drawChancla\(ctx, x, y, w, h, type, rotation\) \{\n\s*ctx\.save\(\);\n\s*ctx\.translate\(x, y\);",
        r"function drawChancla(ctx, x, y, w, h, type, rotation, c) {\n                ctx.save();\n                if (c && c.invisible) { ctx.globalAlpha = 0; }\n                ctx.translate(x, y);",
        content
    )

    # 8. Ghost emoji
    content = re.sub(
        r"(else if \(type === 'sniper'\) emoji = '🎯';)",
        r"\1\n                else if (type === 'ghost') emoji = '👻';",
        content
    )

    # 9. drawChanclasAll logic
    content = re.sub(
        r"for \(const c of chanclas\) drawChancla\(ctx, c\.x, c\.y, c\.w, c\.h, c\.type, c\.rotation\);",
        r"for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation, c);",
        content
    )

    # 10. Ghost trySlap rewards
    ghost_rewards = r"""} else if (c.type === 'ghost') {
                            gameData.coins += Math.floor(5 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(5 * getPrestigeMultiplier());
                            score += Math.floor(150 * getPrestigeMultiplier());
                            addFloatText('GHOST BUSTED! 👻', c.x, c.y, '#ffffff');
                        } else if (isPerfect) {"""

    content = re.sub(
        r"\} else if \(isPerfect\) \{",
        ghost_rewards,
        content
    )

    with open(filepath, 'w') as f:
        f.write(content)

update_file('index.html')
update_file('chancla_bomb.html')
