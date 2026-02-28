import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    search = """                    if (c.x < 10) { c.x = 10; c.vx *= -0.5; }
                    if (c.x > canvas.width - 10) { c.x = canvas.width - 10; c.vx *= -0.5; }

                    if (!c.slapped && rectsOverlap(player, c)) {"""

    replace = """                    if (c.x < 10) { c.x = 10; c.vx *= -0.5; }
                    if (c.x > canvas.width - 10) { c.x = canvas.width - 10; c.vx *= -0.5; }

                    if (!c.slapped) {
                        const distToPlayer = Math.sqrt(Math.pow(c.x - player.x, 2) + Math.pow(c.y - player.y, 2));
                        if (distToPlayer < 75 && !rectsOverlap(player, c) && !c.grazed) {
                            c.grazed = true;
                            score += 15;
                            specialAttackBar = Math.min(maxSpecialAttack, specialAttackBar + 2);
                            playSound(1500, 0.1);
                            addFloatText('GRAZE! +15', c.x, c.y - 30);
                            for (let k = 0; k < 3; k++) {
                                rosePetals.push({
                                    x: c.x + (Math.random() - 0.5) * 20,
                                    y: c.y + (Math.random() - 0.5) * 20,
                                    vx: (Math.random() - 0.5) * 50,
                                    vy: (Math.random() - 0.5) * 50,
                                    rotation: Math.random() * Math.PI * 2,
                                    rotSpeed: (Math.random() - 0.5) * 5,
                                    emoji: '✨',
                                    size: 16
                                });
                            }
                        }
                    }

                    if (!c.slapped && rectsOverlap(player, c)) {"""

    if search in content:
        content = content.replace(search, replace)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath} successfully")
    else:
        print(f"Search string not found in {filepath}")

patch_file('index.html')
patch_file('chancla_bomb.html')
