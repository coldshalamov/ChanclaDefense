import re

files = ['index.html', 'chancla_bomb.html']

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Old logic arrays
    old_array = """                    const upgrades = [
                        { id: 'lives', cost: 100 },
                        { id: 'shield', cost: 150 },
                        { id: 'cooldown', cost: 200 }
                    ];"""

    new_array = """                    const upgrades = [
                        { id: 'lives', baseCost: 100, maxLevel: 5 },
                        { id: 'shield', baseCost: 150, maxLevel: 5 },
                        { id: 'cooldown', baseCost: 200, maxLevel: 5 },
                        { id: 'speed', baseCost: 150, maxLevel: 10 }
                    ];"""

    # Needs two replacements, one for click, one for touchstart
    content = content.replace(old_array, new_array)


    # Click replace
    old_click = """                            if (!gameData.upgrades[u.id] && gameData.coins >= u.cost) {
                                gameData.coins -= u.cost;
                                gameData.upgrades[u.id] = true;
                                saveGameData();
                                playSound(1200, 0.1); // Cha-ching!
                            } else {
                                playSound(200, 0.1); // Error sound
                            }"""

    new_click = """                            const level = gameData.upgrades[u.id];
                            const cost = Math.floor(u.baseCost * Math.pow(1.5, level));
                            if (level < u.maxLevel && gameData.coins >= cost) {
                                gameData.coins -= cost;
                                gameData.upgrades[u.id]++;
                                saveGameData();
                                playSound(1200, 0.1); // Cha-ching!
                            } else {
                                playSound(200, 0.1); // Error sound
                            }"""

    content = content.replace(old_click, new_click)

    # Touch replace
    old_touch = """                            if (!gameData.upgrades[u.id] && gameData.coins >= u.cost) {
                                gameData.coins -= u.cost;
                                gameData.upgrades[u.id] = true;
                                saveGameData();
                                playSound(1200, 0.1);
                            }"""

    new_touch = """                            const level = gameData.upgrades[u.id];
                            const cost = Math.floor(u.baseCost * Math.pow(1.5, level));
                            if (level < u.maxLevel && gameData.coins >= cost) {
                                gameData.coins -= cost;
                                gameData.upgrades[u.id]++;
                                saveGameData();
                                playSound(1200, 0.1);
                            }"""

    content = content.replace(old_touch, new_touch)


    with open(filepath, 'w') as f:
        f.write(content)

print("Patch applied.")
