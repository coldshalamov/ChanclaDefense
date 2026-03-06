import re

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Update initialization
    init_search = """            let gameData = { coins: 0, upgrades: { lives: false, shield: false, cooldown: false }, bestScore: 0 };
            try {
                const saved = localStorage.getItem('chancla_bomb_save');
                if (saved) gameData = JSON.parse(saved);
                if (!gameData.upgrades) gameData.upgrades = { lives: false, shield: false, cooldown: false };
                if (gameData.coins === undefined) gameData.coins = 0;
                if (gameData.bestScore === undefined) gameData.bestScore = 0;
            } catch (e) { console.error(e); }"""

    init_replace = """            let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0 };
            try {
                const saved = localStorage.getItem('chancla_bomb_save');
                if (saved) {
                    gameData = JSON.parse(saved);
                    // Migrate old boolean upgrades to integer levels
                    if (gameData.upgrades) {
                        for (let key in gameData.upgrades) {
                            if (typeof gameData.upgrades[key] === 'boolean') {
                                gameData.upgrades[key] = gameData.upgrades[key] ? 1 : 0;
                            }
                        }
                    }
                }
                if (!gameData.upgrades) gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0 };
                // Ensure new upgrades exist
                if (gameData.upgrades.speed === undefined) gameData.upgrades.speed = 0;

                if (gameData.coins === undefined) gameData.coins = 0;
                if (gameData.bestScore === undefined) gameData.bestScore = 0;
            } catch (e) { console.error(e); }"""

    content = content.replace(init_search, init_replace)

    # Update player setup in resetGame
    reset_search = """                player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);
                player.shield = gameData.upgrades.shield;"""
    reset_replace = """                player.maxLives = 5 + gameData.upgrades.lives;
                player.lives = 3 + gameData.upgrades.lives;
                player.shield = gameData.upgrades.shield > 0;
                player.speed = 230 + (gameData.upgrades.speed * 15);"""
    content = content.replace(reset_search, reset_replace)

    # Update trySlap cooldown logic
    slap_search = """                if (slappedAny) {
                    slapCooldown = gameData.upgrades.cooldown ? 0.27 : 0.3;
                } else {"""
    slap_replace = """                if (slappedAny) {
                    slapCooldown = 0.3 - (gameData.upgrades.cooldown * 0.015);
                } else {"""
    content = content.replace(slap_search, slap_replace)

    # Update drawShop
    draw_shop_search = """                const upgrades = [
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

    draw_shop_replace = """                const upgrades = [
                    { id: 'lives', name: 'Extra Life (+1)', icon: '❤️', baseCost: 100, maxLevel: 5, desc: 'Start with more lives' },
                    { id: 'shield', name: 'Start Shield', icon: '🛡️', baseCost: 150, maxLevel: 1, desc: 'Start with shield' },
                    { id: 'cooldown', name: 'Fast Hands', icon: '⚡', baseCost: 200, maxLevel: 5, desc: '-5% Slap Cooldown/lvl' },
                    { id: 'speed', name: 'Running Shoes', icon: '👟', baseCost: 120, maxLevel: 5, desc: '+15 Speed/lvl' }
                ];

                let y = 160;
                upgrades.forEach(u => {
                    const level = gameData.upgrades[u.id] || 0;
                    const maxed = level >= u.maxLevel;
                    const currentCost = Math.floor(u.baseCost * Math.pow(1.5, level));
                    const affordable = !maxed && gameData.coins >= currentCost;

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
                    ctx.fillText(`${u.name} (Lv.${level}/${u.maxLevel})`, 100, y + 30);
                    ctx.font = '14px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(u.desc, 100, y + 55);

                    // Cost / Status
                    ctx.textAlign = 'right';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillStyle = '#fff';
                    if (maxed) {
                        ctx.fillText('MAXED', canvas.width - 55, y + 45);
                    } else {
                        ctx.fillText('💰 ' + currentCost, canvas.width - 55, y + 45);
                    }

                    y += 100;
                });"""
    content = content.replace(draw_shop_search, draw_shop_replace)

    # Update click handler for shop
    click_shop_search = """                    // Check Upgrade Buttons
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

    click_shop_replace = """                    // Check Upgrade Buttons
                    const upgrades = [
                        { id: 'lives', baseCost: 100, maxLevel: 5 },
                        { id: 'shield', baseCost: 150, maxLevel: 1 },
                        { id: 'cooldown', baseCost: 200, maxLevel: 5 },
                        { id: 'speed', baseCost: 120, maxLevel: 5 }
                    ];
                    let y = 160;
                    // Button height 80, margin 20
                    for (let u of upgrades) {
                        if (pos.y >= y && pos.y <= y + 80 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            const level = gameData.upgrades[u.id] || 0;
                            const currentCost = Math.floor(u.baseCost * Math.pow(1.5, level));
                            if (level < u.maxLevel && gameData.coins >= currentCost) {
                                gameData.coins -= currentCost;
                                gameData.upgrades[u.id] = level + 1;
                                saveGameData();
                                playSound(1200, 0.1); // Cha-ching!
                            } else {
                                playSound(200, 0.1); // Error sound
                            }
                        }
                        y += 100;
                    }"""
    content = content.replace(click_shop_search, click_shop_replace)

    # Update touchstart handler for shop
    touch_shop_search = """                     // Check Upgrade Buttons
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

    touch_shop_replace = """                     // Check Upgrade Buttons
                    const upgrades = [
                        { id: 'lives', baseCost: 100, maxLevel: 5 },
                        { id: 'shield', baseCost: 150, maxLevel: 1 },
                        { id: 'cooldown', baseCost: 200, maxLevel: 5 },
                        { id: 'speed', baseCost: 120, maxLevel: 5 }
                    ];
                    let y = 160;
                    for (let u of upgrades) {
                        if (pos.y >= y && pos.y <= y + 80 && pos.x >= 40 && pos.x <= canvas.width - 40) {
                            const level = gameData.upgrades[u.id] || 0;
                            const currentCost = Math.floor(u.baseCost * Math.pow(1.5, level));
                            if (level < u.maxLevel && gameData.coins >= currentCost) {
                                gameData.coins -= currentCost;
                                gameData.upgrades[u.id] = level + 1;
                                saveGameData();
                                playSound(1200, 0.1);
                            }
                        }
                        y += 100;
                    }"""
    content = content.replace(touch_shop_search, touch_shop_replace)

    with open(filename, 'w') as f:
        f.write(content)
    print(f"Updated {filename}")

update_file('index.html')
update_file('chancla_bomb.html')
