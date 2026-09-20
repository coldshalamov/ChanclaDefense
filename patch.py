import re

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    storm_func = """            function triggerChanclaStorm() {
                for (let i = 0; i < 15; i++) {
                    const spread = (i / 14) - 0.5;
                    const vx = spread * 800;
                    const vy = baseSpeed * 1.2 + Math.random() * 50;
                    chanclas.push({
                        x: isa.x,
                        y: isa.y + 40,
                        vx: vx,
                        vy: vy,
                        w: 32,
                        h: 18,
                        type: 'fire',
                        rotation: 0,
                        rotSpeed: (Math.random() - 0.5) * 20,
                        trickState: 0,
                        trickTimer: 0,
                        sniperTimer: 0
                    });
                }
            }

            function spawnChancla() {"""

    content = content.replace("            function spawnChancla() {", storm_func, 1)

    enrage_endless_search = """                        addFloatText('¡ENRAGED!', isa.x, isa.y - 30);
                    }
                } else {"""
    enrage_endless_replace = """                        addFloatText('¡ENRAGED!', isa.x, isa.y - 30);
                        triggerChanclaStorm();
                    }
                } else {"""
    content = content.replace(enrage_endless_search, enrage_endless_replace, 1)

    enrage_normal_search = """                    addFloatText('¡ENRAGED!', isa.x, isa.y - 30);
                }"""
    enrage_normal_replace = """                    addFloatText('¡ENRAGED!', isa.x, isa.y - 30);
                    triggerChanclaStorm();
                }"""
    # Just to be safe, replace the second instance or find the exact block

    with open(filepath, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
