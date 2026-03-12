import re

with open('index.html', 'r') as f:
    content = f.read()

old_block = """                const upgrades = [
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

new_block = """                const upgrades = [
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

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("Success patch_drawShop")
else:
    print("Old block not found for drawShop!")
