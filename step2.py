trick_logic = """                    // Trick Logic
                    if (c.type === 'trick' && !c.slapped) {
                        if (c.trickState === 0) {
                            if (c.y > canvas.height * 0.4) {
                                c.trickState = 1;
                                c.trickTimer = 0.5;
                                c.vx_saved = c.vx;
                                c.vy_saved = c.vy;
                                c.vx = 0;
                                c.vy = 0;
                            }
                        } else if (c.trickState === 1) {
                            c.trickTimer -= dt;
                            c.x += (Math.random() - 0.5) * 8; // Vibrate
                            if (c.trickTimer <= 0) {
                                c.trickState = 2;
                                const speed = Math.sqrt(c.vx_saved*c.vx_saved + c.vy_saved*c.vy_saved) * 1.5;
                                const angle = Math.atan2(player.y - c.y, player.x - c.x);
                                c.vx = Math.cos(angle) * speed;
                                c.vy = Math.sin(angle) * speed;
                            }
                        }
                    }

                    // Homing Logic"""

import os
files = ['index.html', 'chancla_bomb.html']
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace("// Homing Logic", trick_logic)
    content = content.replace("if (c.type === 'golden') damage = 0; // Prevent double-dipping as damage is applied in trySlap", "if (c.type === 'golden') damage = 0; // Prevent double-dipping as damage is applied in trySlap\n                            if (c.type === 'trick') damage = 0; // Prevent double dipping")

    with open(filepath, 'w') as f:
        f.write(content)
