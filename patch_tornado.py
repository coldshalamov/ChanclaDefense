import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add isa.tornadoCooldown and isa.tornadoState to resetGame
    reset_target = """                isa.y = 70;
                isa.enraged = false;"""
    reset_patch = """                isa.y = 70;
                isa.enraged = false;
                isa.tornadoCooldown = 15;
                isa.tornadoState = 0;"""
    if reset_target in content:
        content = content.replace(reset_target, reset_patch)
    else:
        print(f"Failed to patch resetGame in {filepath}")

    # 2. Add tornado trigger logic to update
    update_target = """                if (isa.enraged) {
                    meteorTimer += enemyDt;
                    if (meteorTimer >= 12 && !chanclas.some(c => c.type === 'meteor')) {
                        spawnMeteor();
                        meteorTimer = 0;
                    }
                }"""
    update_patch = """                if (isa.enraged) {
                    meteorTimer += enemyDt;
                    if (meteorTimer >= 12 && !chanclas.some(c => c.type === 'meteor')) {
                        spawnMeteor();
                        meteorTimer = 0;
                    }

                    if (isa.tornadoState === 0) {
                        isa.tornadoCooldown -= enemyDt;
                        if (isa.tornadoCooldown <= 0) {
                            isa.tornadoState = 1;
                            isa.tornadoTimer = 5;
                            addFloatText('CHANCLA-NADO! 🌪️', isa.x, isa.y + 50, '#00ffff', 22);
                            playSound(900, 0.5);
                        }
                    } else if (isa.tornadoState === 1) {
                        isa.tornadoTimer -= enemyDt;
                        // Pull chanclas in
                        chanclas.forEach(c => {
                            if (!c.slapped && c.type !== 'meteor' && c.type !== 'sniper') {
                                const dx = isa.x - c.x;
                                const dy = (isa.y + 100) - c.y; // Tornado center
                                c.vx += dx * 5 * enemyDt;
                                c.vy += dy * 5 * enemyDt;
                                c.rotSpeed = 20;
                            }
                        });

                        if (isa.tornadoTimer <= 0) {
                            // Explode
                            isa.tornadoState = 0;
                            isa.tornadoCooldown = 20;
                            playSound(1200, 0.4);
                            triggerShake(20, 0.5);
                            triggerFlash(0.3, '#fff');

                            chanclas.forEach(c => {
                                if (!c.slapped && c.type !== 'meteor' && c.type !== 'sniper') {
                                    const angle = Math.random() * Math.PI * 2;
                                    const speed = 300 + Math.random() * 200;
                                    c.vx = Math.cos(angle) * speed;
                                    c.vy = Math.sin(angle) * speed;
                                }
                            });
                        }
                    }
                }"""
    if update_target in content:
        content = content.replace(update_target, update_patch)
    else:
        print(f"Failed to patch update in {filepath}")

    # 3. Add drawTornado call to draw
    draw_target = """                drawFireParticles();
                drawChanclasAll();"""
    draw_patch = """                drawFireParticles();
                if (isa.tornadoState === 1) drawTornado();
                drawChanclasAll();"""
    if draw_target in content:
        content = content.replace(draw_target, draw_patch)
    else:
        print(f"Failed to patch draw in {filepath}")

    # 4. Add drawTornado function
    draw_func_target = """            function drawChanclasAll() {"""
    draw_func_patch = """            function drawTornado() {
                ctx.save();
                const tornadoX = isa.x;
                const tornadoY = isa.y + 100;

                const t = timeElapsed * 10;
                const radius = 60 + Math.sin(t) * 10;

                ctx.translate(tornadoX, tornadoY);

                for (let i = 0; i < 5; i++) {
                    const angle = t + (i * Math.PI * 2) / 5;
                    const h = -30 + i * 15;
                    const w = radius - Math.abs(h);

                    ctx.beginPath();
                    ctx.ellipse(0, h, w, 10, 0, 0, Math.PI * 2);
                    ctx.strokeStyle = `rgba(0, 255, 255, ${0.3 + (i*0.1)})`;
                    ctx.lineWidth = 3 + (i%2);
                    ctx.stroke();
                }
                ctx.restore();
            }

            function drawChanclasAll() {"""
    if draw_func_target in content:
        content = content.replace(draw_func_target, draw_func_patch)
    else:
        print(f"Failed to patch drawTornado in {filepath}")

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
