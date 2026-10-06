import re

def remove_fiesta(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove variables
    content = re.sub(r'\s*let fiestaMode = false;\n\s*let fiestaHue = 0;', '', content)

    # 2. Remove resets in resetGame
    content = re.sub(r'\s*fiestaMode = false;\n\s*fiestaHue = 0;', '', content)

    # 3. Remove from drawBackground
    bg_block = """                if (fiestaMode) {
                    grad.addColorStop(0, `hsl(${Math.floor(fiestaHue)}, 80%, 30%)`);
                    grad.addColorStop(1, `hsl(${Math.floor((fiestaHue + 60) % 360)}, 80%, 10%)`);
                } else if (isa.enraged) {"""
    content = content.replace(bg_block, "                if (isa.enraged) {")

    # 4. Remove from autoSlap
    content = re.sub(r'const slapRange = fiestaMode \? \d+ : (\d+);', r'const slapRange = \1;', content)
    content = re.sub(r'const perfectRange = fiestaMode \? \d+ : (\d+);', r'const perfectRange = \1;', content)

    # 5. Remove from trySlap cooldown
    content = re.sub(r'\s*if \(fiestaMode\) slapCooldown \*= 0\.5;', '', content)

    # 6. Remove update block in update(dt)
    update_block = """                if (comboCount >= 10 && !fiestaMode) {
                    fiestaMode = true;
                    playSound(600, 0.4);
                    triggerShake(15, 0.5);
                    addFloatText('¡FIESTA MODE!', player.x, player.y - 60);
                } else if (comboCount < 10 && fiestaMode) {
                    fiestaMode = false;
                }

                if (fiestaMode) {
                    fiestaHue = (fiestaHue + dt * 200) % 360;
                    score += dt * 50 * getPrestigeMultiplier(); // passive score

                    // Spawn confetti
                    if (Math.random() < 0.2) {
                        const emojis = ['🎉', '✨', '🎊'];
                        const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                        rosePetals.push({
                            x: Math.random() * canvas.width,
                            y: -20,
                            vx: (Math.random() - 0.5) * 100,
                            vy: 100 + Math.random() * 200,
                            rotation: Math.random() * Math.PI * 2,
                            rotSpeed: (Math.random() - 0.5) * 5,
                            emoji: emoji,
                            size: 15 + Math.random() * 15,
                            life: 3
                        });
                    }
                }"""
    content = content.replace(update_block, "")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Removed fiesta from {filepath}")

remove_fiesta('index.html')
remove_fiesta('chancla_bomb.html')
