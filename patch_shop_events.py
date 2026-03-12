import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace the click listener shop logic
old_click_logic = """                    // Check Upgrade Buttons
                    const upgrades = [
                        { id: 'lives', cost: 100 },
                        { id: 'shield', cost: 150 },
                        { id: 'cooldown', cost: 200 }
                    ];
                    let y = 160;
                    // Button height 80, margin 20
                    for (let u of upgrades) {
                        if (pos.y >= y && pos.y <= y + 80 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            if (!gameData.upgrades[u.id] && gameData.coins >= u.cost) {
                                gameData.coins -= u.cost;
                                gameData.upgrades[u.id] = true;
                                saveGameData();
                                playSound(1200, 0.1); // Cha-ching!
                            } else {
                                playSound(200, 0.1); // Error sound
                            }
                        }
                        y += 100;
                    }"""

new_click_logic = """                    // Check Upgrade Buttons
                    const upgrades = [
                        { id: 'lives', baseCost: 100, maxLevel: 5 },
                        { id: 'shield', baseCost: 150, maxLevel: 5 },
                        { id: 'cooldown', baseCost: 200, maxLevel: 5 },
                        { id: 'speed', baseCost: 150, maxLevel: 5 }
                    ];
                    let y = 160;
                    // Button height 80, margin 20
                    for (let u of upgrades) {
                        if (pos.y >= y && pos.y <= y + 80 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            const level = gameData.upgrades[u.id] || 0;
                            const cost = Math.floor(u.baseCost * Math.pow(1.5, level));
                            if (level < u.maxLevel && gameData.coins >= cost) {
                                gameData.coins -= cost;
                                gameData.upgrades[u.id] = level + 1;
                                saveGameData();
                                playSound(1200, 0.1); // Cha-ching!
                            } else {
                                playSound(200, 0.1); // Error sound
                            }
                        }
                        y += 100;
                    }"""

if old_click_logic in content:
    content = content.replace(old_click_logic, new_click_logic, 1)
    print("Success patch_click")
else:
    print("Old block not found for click logic!")

# Replace the touch listener shop logic
old_touch_logic = """                     // Check Upgrade Buttons
                    const upgrades = [
                        { id: 'lives', cost: 100 },
                        { id: 'shield', cost: 150 },
                        { id: 'cooldown', cost: 200 }
                    ];
                    let y = 160;
                    for (let u of upgrades) {
                        if (pos.y >= y && pos.y <= y + 80 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            if (!gameData.upgrades[u.id] && gameData.coins >= u.cost) {
                                gameData.coins -= u.cost;
                                gameData.upgrades[u.id] = true;
                                saveGameData();
                                playSound(1200, 0.1);
                            }
                        }
                        y += 100;
                    }"""

new_touch_logic = """                     // Check Upgrade Buttons
                    const upgrades = [
                        { id: 'lives', baseCost: 100, maxLevel: 5 },
                        { id: 'shield', baseCost: 150, maxLevel: 5 },
                        { id: 'cooldown', baseCost: 200, maxLevel: 5 },
                        { id: 'speed', baseCost: 150, maxLevel: 5 }
                    ];
                    let y = 160;
                    for (let u of upgrades) {
                        if (pos.y >= y && pos.y <= y + 80 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            const level = gameData.upgrades[u.id] || 0;
                            const cost = Math.floor(u.baseCost * Math.pow(1.5, level));
                            if (level < u.maxLevel && gameData.coins >= cost) {
                                gameData.coins -= cost;
                                gameData.upgrades[u.id] = level + 1;
                                saveGameData();
                                playSound(1200, 0.1);
                            } else {
                                playSound(200, 0.1);
                            }
                        }
                        y += 100;
                    }"""

if old_touch_logic in content:
    content = content.replace(old_touch_logic, new_touch_logic, 1)
    print("Success patch_touch")
else:
    print("Old block not found for touch logic!")

with open('index.html', 'w') as f:
    f.write(content)
