with open("index.html", "r") as f:
    content = f.read()

search_str = """                        if (isPerfect) {
                            gameData.coins += Math.floor(2 * getPrestigeMultiplier());"""

replace_str = """                        if (c.type === 'golden') {
                            gameData.coins += Math.floor(25 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(25 * getPrestigeMultiplier());
                            score += Math.floor(500 * getPrestigeMultiplier());
                            addFloatText('GOLDEN SLAP! +25💰✨', c.x, c.y - 10, '#ffd700', 16);
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.2);
                            triggerShake(10, 0.3);
                            triggerFlash(0.3, '#ffd700');
                            hitStop = 0.2;
                            spawnRoseExplosion(c.x, c.y);

                            // Reflect all other active chanclas
                            for (let j = 0; j < chanclas.length; j++) {
                                const other = chanclas[j];
                                if (!other.slapped && other !== c && other.type !== 'meteor') {
                                    other.slapped = true;
                                    other.vx = (isa.x - other.x) * 2;
                                    other.vy = -600;
                                }
                            }
                        } else if (isPerfect) {
                            gameData.coins += Math.floor(2 * getPrestigeMultiplier());"""

if search_str in content:
    content = content.replace(search_str, replace_str)
    with open("index.html", "w") as f:
        f.write(content)
    print("Part 2 Success!")
else:
    print("Part 2 Failed: string not found")
