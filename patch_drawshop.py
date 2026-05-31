import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Title and coins Y coordinates
    content = content.replace("ctx.fillText('SHOP / TIENDA', canvas.width / 2, 80);", "ctx.fillText('SHOP / TIENDA', canvas.width / 2, 50);")
    content = content.replace("ctx.fillText('💰 ' + gameData.coins, canvas.width / 2, 120);", "ctx.fillText('💰 ' + gameData.coins, canvas.width / 2, 90);")

    # Add power to upgrades list and update Y logic
    old_upgrades = """                const upgrades = [
                    { id: 'lives', name: 'Extra Life', icon: '❤️', baseCost: 100, maxLevel: 5, desc: '+1 Life per level' },
                    { id: 'shield', name: 'Start Shield', icon: '🛡️', baseCost: 150, maxLevel: 1, desc: 'Start with shield' },
                    { id: 'cooldown', name: 'Fast Hands', icon: '⚡', baseCost: 200, maxLevel: 5, desc: '-15ms Cooldown/lvl' },
                    { id: 'speed', name: 'Dash Speed', icon: '👟', baseCost: 150, maxLevel: 5, desc: '+15 Speed/lvl' }
                ];

                let y = 160;"""
    new_upgrades = """                const upgrades = [
                    { id: 'lives', name: 'Extra Life', icon: '❤️', baseCost: 100, maxLevel: 5, desc: '+1 Life per level' },
                    { id: 'shield', name: 'Start Shield', icon: '🛡️', baseCost: 150, maxLevel: 1, desc: 'Start with shield' },
                    { id: 'cooldown', name: 'Fast Hands', icon: '⚡', baseCost: 200, maxLevel: 5, desc: '-15ms Cooldown/lvl' },
                    { id: 'speed', name: 'Dash Speed', icon: '👟', baseCost: 150, maxLevel: 5, desc: '+15 Speed/lvl' },
                    { id: 'power', name: 'Slap Power', icon: '💪', baseCost: 250, maxLevel: 5, desc: '+Damage to Isa' }
                ];

                let y = 120;"""
    content = content.replace(old_upgrades, new_upgrades)

    # Change increment
    content = content.replace("y += 100;", "y += 95;")

    # ensure we only replaced the increment inside drawShop, there might be other y += 100
    # Actually wait let's use regex or more precise replacement for increment

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Patched drawShop")
