trick_slap = """                        } else if (c.type === 'trick') {
                            gameData.coins += Math.floor(2 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(2 * getPrestigeMultiplier());
                            score += Math.floor(15 * getPrestigeMultiplier());
                            triggerFlash(0.2, '#ff00ff');
                            addFloatText('TRICKED! 🃏', c.x, c.y, '#ff00ff');
                            isa.anger = Math.max(0, isa.anger - 10);
                            if (isa.anger <= 0) triggerWin();
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.2);
                        } else if (isPerfect) {"""

import os
files = ['index.html', 'chancla_bomb.html']
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace("} else if (isPerfect) {", trick_slap)
    with open(filepath, 'w') as f:
        f.write(content)
