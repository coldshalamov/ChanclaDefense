import re

with open('chancla_bomb.html', 'r') as f:
    content = f.read()

# 1. gameData
old_gameData = """            let gameData = { coins: 0, upgrades: { lives: false, shield: false, cooldown: false }, bestScore: 0 };
            try {
                const saved = localStorage.getItem('chancla_bomb_save');
                if (saved) gameData = JSON.parse(saved);
                if (!gameData.upgrades) gameData.upgrades = { lives: false, shield: false, cooldown: false };
                if (gameData.coins === undefined) gameData.coins = 0;
                if (gameData.bestScore === undefined) gameData.bestScore = 0;
            } catch (e) { console.error(e); }"""

new_gameData = """            let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0 };
            try {
                const saved = localStorage.getItem('chancla_bomb_save');
                if (saved) gameData = JSON.parse(saved);
                if (!gameData.upgrades) gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0 };

                // Migrate old boolean saves to integer levels
                if (typeof gameData.upgrades.lives === 'boolean') gameData.upgrades.lives = gameData.upgrades.lives ? 1 : 0;
                if (typeof gameData.upgrades.shield === 'boolean') gameData.upgrades.shield = gameData.upgrades.shield ? 1 : 0;
                if (typeof gameData.upgrades.cooldown === 'boolean') gameData.upgrades.cooldown = gameData.upgrades.cooldown ? 1 : 0;

                // Initialize missing upgrades
                if (gameData.upgrades.speed === undefined) gameData.upgrades.speed = 0;
                if (gameData.coins === undefined) gameData.coins = 0;
                if (gameData.bestScore === undefined) gameData.bestScore = 0;
            } catch (e) { console.error(e); }"""

if old_gameData in content:
    content = content.replace(old_gameData, new_gameData, 1)
    print("Success patch_gameData")
else:
    print("Old block not found for gameData!")

# 2. drawShop
old_drawShop = """                const upgrades = [
                    { id: 'lives', name: 'Extra Life (+1)', icon: '❤️', cost: 100, desc: 'Start with 4 lives' },
                    { id: 'shield', name: 'Start Shield', icon: '🛡️', cost: 150, desc: 'Start with shield' },
                    { id: 'cooldown', name: 'Fast Hands', icon: '⚡', cost: 200, desc: '-10% Slap Cooldown' }
                ];

                let y = 160;
                upgrades.forEach(u => {
                    const owned = gameData.upgrades[u.id];
                    const affordable = gameData.coins >= u.cost;

                    // Button bg
                    ctx.fillStyle = owned ? '#4caf50' : (affordable ? '#2196f3' : '#555');
                    roundRect(ctx, 40, y, canvas.width - 80, 80, 10);
                    ctx.fill();

                    // Border
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    roundRect(ctx, 40, y, canvas.width - 80, 80, 10);
                    ctx.stroke();

                    // Icon
                    ctx.font = '30px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#fff';
                    ctx.fillText(u.icon, 55, y + 50);

                    // Text
                    ctx.font = 'bold 18px sans-serif';
                    ctx.fillText(u.name, 100, y + 30);
                    ctx.font = '14px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(u.desc, 100, y + 55);

                    // Cost / Status
                    ctx.textAlign = 'right';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillStyle = '#fff';
                    if (owned) {
                        ctx.fillText('OWNED', canvas.width - 55, y + 45);
                    } else {
                        ctx.fillText('💰 ' + u.cost, canvas.width - 55, y + 45);
                    }

                    y += 100;
                });"""

new_drawShop = """                const upgrades = [
                    { id: 'lives', name: 'Extra Life', icon: '❤️', baseCost: 100, maxLevel: 5, desc: '+1 Starting life' },
                    { id: 'shield', name: 'Start Shield', icon: '🛡️', baseCost: 150, maxLevel: 5, desc: 'Start with shield' },
                    { id: 'cooldown', name: 'Fast Hands', icon: '⚡', baseCost: 200, maxLevel: 5, desc: 'Reduce slap cooldown' },
                    { id: 'speed', name: 'Swift Feet', icon: '👟', baseCost: 150, maxLevel: 5, desc: '+ Speed' }
                ];

                let y = 160;
                upgrades.forEach(u => {
                    const level = gameData.upgrades[u.id] || 0;
                    const maxed = level >= u.maxLevel;
                    const cost = Math.floor(u.baseCost * Math.pow(1.5, level));
                    const affordable = gameData.coins >= cost;

                    // Button bg
                    ctx.fillStyle = maxed ? '#4caf50' : (affordable ? '#2196f3' : '#555');
                    roundRect(ctx, 40, y, canvas.width - 80, 80, 10);
                    ctx.fill();

                    // Border
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    roundRect(ctx, 40, y, canvas.width - 80, 80, 10);
                    ctx.stroke();

                    // Icon
                    ctx.font = '30px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#fff';
                    ctx.fillText(u.icon, 55, y + 50);

                    // Text
                    ctx.font = 'bold 18px sans-serif';
                    ctx.fillText(u.name + ` (Lvl ${level}/${u.maxLevel})`, 100, y + 30);
                    ctx.font = '14px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(u.desc, 100, y + 55);

                    // Cost / Status
                    ctx.textAlign = 'right';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillStyle = '#fff';
                    if (maxed) {
                        ctx.fillText('MAX', canvas.width - 55, y + 45);
                    } else {
                        ctx.fillText('💰 ' + cost, canvas.width - 55, y + 45);
                    }

                    y += 100;
                });"""

if old_drawShop in content:
    content = content.replace(old_drawShop, new_drawShop, 1)
    print("Success patch_drawShop")
else:
    print("Old block not found for drawShop!")

# 3. resetGame
old_resetGame = """            function resetGame() {
                player.x = canvas.width / 2;
                player.y = canvas.height - 70;
                player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);
                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;
                isa.anger = isa.maxAnger;
                isa.x = canvas.width / 2;"""

new_resetGame = """            function resetGame() {
                player.x = canvas.width / 2;
                player.y = canvas.height - 70;
                player.lives = 3 + (gameData.upgrades.lives || 0);
                player.maxLives = 5 + (gameData.upgrades.lives || 0);
                player.shield = (gameData.upgrades.shield || 0) > 0;
                player.speed = 230 + (gameData.upgrades.speed || 0) * 15;
                player.hitTimer = 0;
                isa.anger = isa.maxAnger;
                isa.x = canvas.width / 2;"""

if old_resetGame in content:
    content = content.replace(old_resetGame, new_resetGame, 1)
    print("Success patch_resetGame")
else:
    print("Old block not found for resetGame!")

# 4. trySlap
old_trySlap = """                if (slappedAny) {
                    slapCooldown = gameData.upgrades.cooldown ? 0.27 : 0.3;
                } else {
                    slapCooldown = 0.15;"""

new_trySlap = """                if (slappedAny) {
                    const cooldownReduction = (gameData.upgrades.cooldown || 0) * 0.015;
                    slapCooldown = Math.max(0.1, 0.3 - cooldownReduction);
                } else {
                    slapCooldown = 0.15;"""

if old_trySlap in content:
    content = content.replace(old_trySlap, new_trySlap, 1)
    print("Success patch_trySlap")
else:
    print("Old block not found for trySlap!")

# 5. Click listener shop logic
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

# 6. Touch listener shop logic
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

with open('chancla_bomb.html', 'w') as f:
    f.write(content)
