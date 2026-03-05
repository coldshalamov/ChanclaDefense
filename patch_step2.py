import re

with open('index.html', 'r') as f:
    content = f.read()

# Update applyPowerup
taco_logic = """                if (p.kind === 'taco') {
                    // Taco Bomb clears all chanclas
                    if (chanclas.length > 0) {
                        for (let i = chanclas.length - 1; i >= 0; i--) {
                            const c = chanclas[i];
                            spawnImpact(c.x, c.y);
                            score += 5;
                            comboCount++;
                            chanclas.splice(i, 1);
                        }
                        shakeTimer = 0.5;
                        flash.timer = 0.2;
                        flash.color = '#ffffff';
                        playSound(200, 0.3);
                        addFloatText('TACO BOMB! 🌮💥', p.x, p.y);
                        sayRandom('super'); // reuse super dialogue or generic
                    } else {
                        addFloatText('🌮 (Mmm...)', p.x, p.y);
                        score += 5;
                    }
                }"""

chili_logic = """                if (p.kind === 'chili') {
                    player.chiliTimer = 6;
                    addFloatText('SPICY MODE! 🌶️', p.x, p.y);
                    sayRandom('super');
                }"""
content = content.replace(taco_logic, chili_logic)

# Update owen
owen_logic = "const type = r < 0.2 ? 'phone' : (r < 0.45 ? 'taco' : 'beer');"
owen_chili_logic = "const type = r < 0.2 ? 'phone' : (r < 0.45 ? 'chili' : 'beer');"
content = content.replace(owen_logic, owen_chili_logic)

with open('index.html', 'w') as f:
    f.write(content)
