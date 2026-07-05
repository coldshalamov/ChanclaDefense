import re

files = ['index.html', 'chancla_bomb.html']

click_prestige = """                } else if (state === STATE.PRESTIGE) {
                    if (pos.y >= 350 && pos.y <= 420 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        playSound(1200, 0.1);
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                } else if (state === STATE.COSMETICS) {"""

touch_prestige = """                if (state === STATE.PRESTIGE) {
                    if (pos.y >= 350 && pos.y <= 420 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                        gameData.prestige = (gameData.prestige || 0) + 1;
                        gameData.stats.wins = 1;
                        gameData.coins = 0;
                        gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 };
                        saveGameData();
                        playSound(1200, 0.1);
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                    if (pos.y >= canvas.height - 100 && pos.y <= canvas.height - 50 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        setDirectionsVisible(true);
                        state = STATE.TITLE;
                    }
                }
                if (state === STATE.COSMETICS) {"""

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # For click handler
    content = content.replace("                } else if (state === STATE.COSMETICS) {", click_prestige)

    # For touch handler (this looks for the one without the leading '}')
    content = content.replace("                if (state === STATE.COSMETICS) {", touch_prestige)

    with open(filename, 'w') as f:
        f.write(content)

print("Step 5 done")
