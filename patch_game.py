import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update gameData initial state and migration
    old_gameData = """            let gameData = { coins: 0, upgrades: { lives: false, shield: false, cooldown: false }, bestScore: 0 };
            try {
                const saved = localStorage.getItem('chancla_bomb_save');
                if (saved) gameData = JSON.parse(saved);
                if (!gameData.upgrades) gameData.upgrades = { lives: false, shield: false, cooldown: false };
                if (gameData.coins === undefined) gameData.coins = 0;
                if (gameData.bestScore === undefined) gameData.bestScore = 0;
            } catch (e) { console.error(e); }"""

    new_gameData = """            let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, luck: 0 }, bestScore: 0 };
            try {
                const saved = localStorage.getItem('chancla_bomb_save');
                if (saved) gameData = JSON.parse(saved);
                if (!gameData.upgrades) gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, luck: 0 };
                // Migration
                for (let k of ['lives', 'shield', 'cooldown']) {
                    if (typeof gameData.upgrades[k] === 'boolean') {
                        gameData.upgrades[k] = gameData.upgrades[k] ? 1 : 0;
                    }
                }
                if (gameData.upgrades.luck === undefined) gameData.upgrades.luck = 0;
                if (gameData.coins === undefined) gameData.coins = 0;
                if (gameData.bestScore === undefined) gameData.bestScore = 0;
            } catch (e) { console.error(e); }"""

    content = content.replace(old_gameData, new_gameData)

    # 2. Update resetGame logic
    old_resetGame = """                player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);
                player.shield = gameData.upgrades.shield;"""
    new_resetGame = """                player.lives = 3 + (gameData.upgrades.lives || 0);
                player.shield = (gameData.upgrades.shield || 0) > 0;"""
    content = content.replace(old_resetGame, new_resetGame)

    # 3. Update drawShop logic
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

    new_drawShop = """                const shopItems = [
                    { id: 'lives', name: 'Extra Life', icon: '❤️', baseCost: 100, costMult: 1.5, maxLevel: 5, desc: '+1 Max Life per level' },
                    { id: 'shield', name: 'Shield', icon: '🛡️', baseCost: 150, costMult: 1.8, maxLevel: 3, desc: 'Start with shield' },
                    { id: 'cooldown', name: 'Fast Hands', icon: '⚡', baseCost: 200, costMult: 1.6, maxLevel: 5, desc: '-10% Slap Cooldown' },
                    { id: 'luck', name: 'Luck', icon: '🍀', baseCost: 150, costMult: 1.5, maxLevel: 5, desc: '+50% Pet Spawns' }
                ];

                let y = 140;
                const itemHeight = 70;
                const spacing = 85;

                shopItems.forEach(u => {
                    const level = gameData.upgrades[u.id] || 0;
                    const maxed = level >= u.maxLevel;
                    const cost = Math.floor(u.baseCost * Math.pow(u.costMult, level));
                    const affordable = gameData.coins >= cost;

                    // Button bg
                    ctx.fillStyle = maxed ? '#4caf50' : (affordable ? '#2196f3' : '#555');
                    roundRect(ctx, 40, y, canvas.width - 80, itemHeight, 10);
                    ctx.fill();

                    // Border
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    roundRect(ctx, 40, y, canvas.width - 80, itemHeight, 10);
                    ctx.stroke();

                    // Icon
                    ctx.font = '24px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillStyle = '#fff';
                    ctx.fillText(u.icon, 55, y + 42);

                    // Text
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillText(`${u.name} (Lv.${level})`, 95, y + 26);
                    ctx.font = '12px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(u.desc, 95, y + 48);

                    // Cost / Status
                    ctx.textAlign = 'right';
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillStyle = '#fff';
                    if (maxed) {
                        ctx.fillText('MAX', canvas.width - 55, y + 40);
                    } else {
                        ctx.fillText('💰 ' + cost, canvas.width - 55, y + 40);
                    }

                    y += spacing;
                });"""
    content = content.replace(old_drawShop, new_drawShop)

    # 4. Update trySlap cooldown
    old_trySlap = """                if (slappedAny) {
                    slapCooldown = gameData.upgrades.cooldown ? 0.27 : 0.3;
                } else {"""
    new_trySlap = """                if (slappedAny) {
                    const cdReduction = (gameData.upgrades.cooldown || 0) * 0.10;
                    slapCooldown = 0.3 * (1 - cdReduction);
                } else {"""
    content = content.replace(old_trySlap, new_trySlap)

    # 5. Update update() for pet spawning with luck
    old_luck = """                if (!pets.some(p => p.kind === 'owen') && (player.lives <= 2 && Math.random() < 0.003 || Math.random() < 0.0007)) {
                    spawnOwen();
                }
                if (!pets.some(p => p.kind === 'rita') && Math.random() < 0.0007) {
                    spawnRita();
                }"""
    new_luck = """                const luckMult = 1 + (gameData.upgrades.luck || 0) * 0.5;

                if (!pets.some(p => p.kind === 'owen') && ((player.lives <= 2 && Math.random() < 0.003 * luckMult) || Math.random() < 0.0007 * luckMult)) {
                    spawnOwen();
                }
                if (!pets.some(p => p.kind === 'rita') && Math.random() < 0.0007 * luckMult) {
                    spawnRita();
                }"""
    content = content.replace(old_luck, new_luck)

    # 6. Shop interactions (click)
    old_click = """                    // Check Upgrade Buttons
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
    new_click = """                    // Check Upgrade Buttons
                    const shopItems = [
                        { id: 'lives', baseCost: 100, costMult: 1.5, maxLevel: 5 },
                        { id: 'shield', baseCost: 150, costMult: 1.8, maxLevel: 3 },
                        { id: 'cooldown', baseCost: 200, costMult: 1.6, maxLevel: 5 },
                        { id: 'luck', baseCost: 150, costMult: 1.5, maxLevel: 5 }
                    ];
                    let y = 140;
                    const itemHeight = 70;
                    const spacing = 85;
                    for (let u of shopItems) {
                        if (pos.y >= y && pos.y <= y + itemHeight && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            const level = gameData.upgrades[u.id] || 0;
                            const cost = Math.floor(u.baseCost * Math.pow(u.costMult, level));
                            if (level < u.maxLevel && gameData.coins >= cost) {
                                gameData.coins -= cost;
                                gameData.upgrades[u.id] = level + 1;
                                saveGameData();
                                playSound(1200, 0.1); // Cha-ching!
                            } else {
                                playSound(200, 0.1); // Error sound
                            }
                        }
                        y += spacing;
                    }"""
    content = content.replace(old_click, new_click)

    # 7. Shop interactions (touchstart)
    old_touch = """                     // Check Upgrade Buttons
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
    new_touch = """                     // Check Upgrade Buttons
                    const shopItems = [
                        { id: 'lives', baseCost: 100, costMult: 1.5, maxLevel: 5 },
                        { id: 'shield', baseCost: 150, costMult: 1.8, maxLevel: 3 },
                        { id: 'cooldown', baseCost: 200, costMult: 1.6, maxLevel: 5 },
                        { id: 'luck', baseCost: 150, costMult: 1.5, maxLevel: 5 }
                    ];
                    let y = 140;
                    const itemHeight = 70;
                    const spacing = 85;
                    for (let u of shopItems) {
                        if (pos.y >= y && pos.y <= y + itemHeight && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            const level = gameData.upgrades[u.id] || 0;
                            const cost = Math.floor(u.baseCost * Math.pow(u.costMult, level));
                            if (level < u.maxLevel && gameData.coins >= cost) {
                                gameData.coins -= cost;
                                gameData.upgrades[u.id] = level + 1;
                                saveGameData();
                                playSound(1200, 0.1);
                            }
                        }
                        y += spacing;
                    }"""
    content = content.replace(old_touch, new_touch)

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Patched {filepath}")

process_file('index.html')
process_file('chancla_bomb.html')
