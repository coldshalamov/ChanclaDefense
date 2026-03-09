import re

files = ['index.html', 'chancla_bomb.html']

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace upgrades array in drawShop
    old_upgrades = """                const upgrades = [
                    { id: 'lives', name: 'Extra Life (+1)', icon: '❤️', cost: 100, desc: 'Start with 4 lives' },
                    { id: 'shield', name: 'Start Shield', icon: '🛡️', cost: 150, desc: 'Start with shield' },
                    { id: 'cooldown', name: 'Fast Hands', icon: '⚡', cost: 200, desc: '-10% Slap Cooldown' }
                ];"""

    new_upgrades = """                const upgrades = [
                    { id: 'lives', name: 'Extra Life', icon: '❤️', baseCost: 100, maxLevel: 5, desc: '+1 Max Life per level' },
                    { id: 'shield', name: 'Start Shield', icon: '🛡️', baseCost: 150, maxLevel: 5, desc: 'Start with shield' },
                    { id: 'cooldown', name: 'Fast Hands', icon: '⚡', baseCost: 200, maxLevel: 5, desc: '-10% Slap Cooldown' },
                    { id: 'speed', name: 'Running Shoes', icon: '👟', baseCost: 150, maxLevel: 10, desc: '+Speed per level' }
                ];"""

    content = content.replace(old_upgrades, new_upgrades)

    # Replace upgrade rendering logic
    old_logic = """                    const owned = gameData.upgrades[u.id];
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
                    }"""

    new_logic = """                    const level = gameData.upgrades[u.id];
                    const cost = Math.floor(u.baseCost * Math.pow(1.5, level));
                    const isMax = level >= u.maxLevel;
                    const affordable = !isMax && gameData.coins >= cost;

                    // Button bg
                    ctx.fillStyle = isMax ? '#4caf50' : (affordable ? '#2196f3' : '#555');
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
                    ctx.fillText(u.name + ' (Lv ' + level + ')', 100, y + 30);
                    ctx.font = '14px sans-serif';
                    ctx.fillStyle = '#ddd';
                    ctx.fillText(u.desc, 100, y + 55);

                    // Cost / Status
                    ctx.textAlign = 'right';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillStyle = '#fff';
                    if (isMax) {
                        ctx.fillText('MAX LEVEL', canvas.width - 55, y + 45);
                    } else {
                        ctx.fillText('💰 ' + cost, canvas.width - 55, y + 45);
                    }"""

    content = content.replace(old_logic, new_logic)

    with open(filepath, 'w') as f:
        f.write(content)

print("Patch applied.")
