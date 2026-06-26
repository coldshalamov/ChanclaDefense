def modify_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Step 1: Declare the slowMoTimer variable
    content = content.replace('let hitStop = 0;', 'let hitStop = 0;\n            let slowMoTimer = 0;', 1)

    # Step 2: Reset slowMoTimer when the game resets
    content = content.replace('                hitStop = 0;', '                hitStop = 0;\n                slowMoTimer = 0;', 1)

    # Step 3: Update update(dt) logic to apply slow motion
    update_replacement = """function update(dt) {
                if (state !== STATE.PLAYING) return;

                if (slowMoTimer > 0) {
                    slowMoTimer -= dt;
                    dt *= 0.3;
                }

                if (shakeTimer > 0) {"""
    content = content.replace("""function update(dt) {
                if (state !== STATE.PLAYING) return;

                if (shakeTimer > 0) {""", update_replacement, 1)

    # Step 4: Add cyan tint effect in drawBackground()
    bg_replacement = """                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                if (slowMoTimer > 0) {
                    ctx.fillStyle = 'rgba(0, 255, 255, 0.15)';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                }"""
    content = content.replace("""                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, canvas.width, canvas.height);""", bg_replacement, 1)

    # Step 5: Implement Perfect Dodge logic for projectiles
    dodge_replacement = """                        if (dashTimer > 0) {
                            if (!c.dodged) {
                                c.dodged = true;
                                slowMoTimer = 1.5;
                                addFloatText('PERFECT DODGE!', player.x, player.y - 30, '#00ffff', 16);
                                triggerFlash(0.2, '#00ffff');
                            }
                            continue;
                        }"""
    content = content.replace("""                        if (dashTimer > 0) continue; // I-frames during dash""", dodge_replacement, 1)

    # Step 6: Implement Perfect Dodge logic for shockwaves
    shockwave_replacement = """                        if (dashTimer > 0) {
                            if (!c.dodged) {
                                c.dodged = true;
                                slowMoTimer = 1.5;
                                addFloatText('PERFECT DODGE!', player.x, player.y - 30, '#00ffff', 16);
                                triggerFlash(0.2, '#00ffff');
                            }
                            continue;
                        } // I-frames during dash shockwave"""
    content = content.replace("""                        if (dashTimer > 0) continue; // I-frames during dash shockwave""", shockwave_replacement, 1)

    with open(filename, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
print("Done")
