import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    search_str = """                    if (!c.slapped && rectsOverlap(player, c)) {"""

    replace_str = """                    if (!c.slapped && !c.grazed && !rectsOverlap(player, c)) {
                        const distToPlayer = Math.sqrt(Math.pow(c.x - player.x, 2) + Math.pow(c.y - player.y, 2));
                        if (distToPlayer < 75) {
                            c.grazed = true;
                            score += 15;
                            specialAttackBar = Math.min(100, specialAttackBar + 2);
                            playSound(1500, 0.1);
                            addFloatText('GRAZE! +15', c.x, c.y);
                            rosePetals.push({
                                x: c.x,
                                y: c.y,
                                vy: -50,
                                rotation: Math.random() * Math.PI * 2,
                                rotSpeed: (Math.random() - 0.5) * 5,
                                emoji: '✨',
                                size: 16
                            });
                        }
                    }

                    if (!c.slapped && rectsOverlap(player, c)) {"""

    if search_str not in content:
        print(f"Could not find search string in {filepath}")
        return

    content = content.replace(search_str, replace_str, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('index.html')
patch_file('chancla_bomb.html')
