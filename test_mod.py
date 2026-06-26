import re

def modify_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Add slowMoTimer declaration
    content = content.replace('let hitStop = 0;', 'let hitStop = 0;\n            let slowMoTimer = 0;')

    # Add slowMoTimer reset
    content = content.replace('hitStop = 0;', 'hitStop = 0;\n                slowMoTimer = 0;')

    # Add update(dt) modification
    update_replacement = """function update(dt) {
                if (state !== STATE.PLAYING) return;

                if (slowMoTimer > 0) {
                    slowMoTimer -= dt;
                    dt *= 0.3;
                }

                if (shakeTimer > 0) {"""
    content = content.replace("""function update(dt) {
                if (state !== STATE.PLAYING) return;

                if (shakeTimer > 0) {""", update_replacement)

    # Add cyan tint to drawBackground
    bg_replacement = """                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                if (slowMoTimer > 0) {
                    ctx.fillStyle = 'rgba(0, 255, 255, 0.15)';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                }"""
    content = content.replace("""                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, canvas.width, canvas.height);""", bg_replacement)

    # Add dodge logic
    dodge_replacement = """                        if (dashTimer > 0) {
                            if (!c.dodged) {
                                c.dodged = true;
                                slowMoTimer = 1.5;
                                addFloatText('PERFECT DODGE!', player.x, player.y - 30, '#00ffff', 16);
                                triggerFlash(0.2, '#00ffff');
                            }
                            continue;
                        }"""
    content = content.replace("""                        if (dashTimer > 0) continue; // I-frames during dash""", dodge_replacement)

    with open(filename, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
print("Done")
