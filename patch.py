import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add isa.enraged property to the `isa` object initialization
    # const isa = { x: canvas.width / 2, y: 70, anger: 100, maxAnger: 100, hitTimer: 0, chismeTimer: 0 };
    content = content.replace(
        "const isa = { x: canvas.width / 2, y: 70, anger: 100, maxAnger: 100, hitTimer: 0, chismeTimer: 0 };",
        "const isa = { x: canvas.width / 2, y: 70, anger: 100, maxAnger: 100, hitTimer: 0, chismeTimer: 0, enraged: false };"
    )

    # 2. Add fireParticles array initialization
    # let specialProjectiles = [];
    content = content.replace(
        "let specialProjectiles = [];",
        "let specialProjectiles = [];\n            let fireParticles = [];"
    )

    # 3. Add to resetGame()
    # isa.chismeTimer = 0;
    # chanclas = [];
    # ...
    # specialProjectiles = [];
    # impacts = [];
    content = content.replace(
        "isa.chismeTimer = 0;\n                chanclas = [];",
        "isa.chismeTimer = 0;\n                isa.enraged = false;\n                chanclas = [];"
    )
    content = content.replace(
        "specialProjectiles = [];\n                impacts = [];",
        "specialProjectiles = [];\n                fireParticles = [];\n                impacts = [];"
    )

    # 4. Modify update() to trigger enraged
    # if (hitStop > 0) { ... }
    # timeElapsed += dt;
    content = content.replace(
        "timeElapsed += dt;\n                spawnTimer += dt;",
        """timeElapsed += dt;
                spawnTimer += dt;

                if (isa.anger <= isa.maxAnger * 0.3 && !isa.enraged) {
                    isa.enraged = true;
                    addFloatText('¡ME HACES ENOJAR!', isa.x, isa.y + 40);
                    triggerShake(10, 1.0);
                    playSound(300, 1.0); // ominous sound
                }"""
    )

    # 5. Modify update() to update fireParticles
    # updateChainEffects(dt);
    # // Update rose petals
    content = content.replace(
        "updateChainEffects(dt);\n\n                // Update rose petals",
        """updateChainEffects(dt);

                // Update fire particles
                for (let i = fireParticles.length - 1; i >= 0; i--) {
                    const p = fireParticles[i];
                    p.x += p.vx * dt;
                    p.y += p.vy * dt;
                    p.rotation += p.rotSpeed * dt;
                    p.life -= dt;
                    if (p.life <= 0) {
                        fireParticles.splice(i, 1);
                    }
                }

                // Update rose petals"""
    )

    # 6. Modify drawBackground() for enraged state
    # function drawBackground() {
    #     const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    #     grad.addColorStop(0, '#0b1930');
    #     grad.addColorStop(1, '#0f243a');
    content = content.replace(
        """function drawBackground() {
                const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
                grad.addColorStop(0, '#0b1930');
                grad.addColorStop(1, '#0f243a');""",
        """function drawBackground() {
                const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
                if (isa.enraged) {
                    grad.addColorStop(0, '#3a0f0f');
                    grad.addColorStop(1, '#1a0505');
                } else {
                    grad.addColorStop(0, '#0b1930');
                    grad.addColorStop(1, '#0f243a');
                }"""
    )

    # 7. Modify drawIsa() to show aura and emit fireParticles
    # function drawIsa() {
    #     ctx.save();
    #     let drawX = isa.x;
    #     let drawY = isa.y;
    #     if (isa.hitTimer > 0) {
    content = content.replace(
        """function drawIsa() {
                ctx.save();
                let drawX = isa.x;
                let drawY = isa.y;""",
        """function drawIsa() {
                ctx.save();
                let drawX = isa.x;
                let drawY = isa.y;

                if (isa.enraged && state === STATE.PLAYING) {
                    // Pulsating aura
                    const pulse = Math.sin(timeElapsed * 8) * 0.2 + 0.8;
                    ctx.shadowColor = '#ff3300';
                    ctx.shadowBlur = 30 * pulse;

                    // Spawn fire particles randomly
                    if (Math.random() < 0.2) {
                        fireParticles.push({
                            x: drawX + (Math.random() - 0.5) * 60,
                            y: drawY + (Math.random() - 0.5) * 60,
                            vx: (Math.random() - 0.5) * 40,
                            vy: -30 - Math.random() * 40,
                            rotation: Math.random() * Math.PI * 2,
                            rotSpeed: (Math.random() - 0.5) * 5,
                            emoji: '🔥',
                            size: 15 + Math.random() * 15,
                            life: 0.5 + Math.random() * 0.5
                        });
                    }
                }"""
    )

    # Remove shadowBlur if not enraged but reset is needed? Not necessary since it's wrapped in save/restore, but we need to ensure the aura doesn't affect other things if drawIsa is called.
    # The aura is just shadowBlur, which will apply to the avatar drawing.

    # 8. Add drawFireParticles() function and call it in draw()
    # drawRosePetals();
    # drawChainEffects();
    content = content.replace(
        "drawRosePetals();\n                drawChainEffects();",
        "drawRosePetals();\n                drawFireParticles();\n                drawChainEffects();"
    )

    # Add the function definition before drawRosePetals
    # function drawRosePetals() {
    content = content.replace(
        "function drawRosePetals() {",
        """function drawFireParticles() {
                fireParticles.forEach(p => {
                    ctx.save();
                    ctx.globalAlpha = p.life / 1.0; // Fade out
                    ctx.translate(p.x, p.y);
                    ctx.rotate(p.rotation);
                    ctx.font = (p.size) + 'px "Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", sans-serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(p.emoji, 0, 0);
                    ctx.restore();
                });
            }

            function drawRosePetals() {"""
    )

    # 9. Modify spawnChancla() to spawn fire chanclas and increase speed/rate
    # function spawnChancla() {
    #     const isSuper = superEnabled && Math.random() < 0.18;
    #     const w = isSuper ? 46 : 32;
    #     const h = isSuper ? 26 : 18;
    #     const x = 40 + Math.random() * (canvas.width - 80);
    #     const y = isa.y + 40;
    #     const vy = baseSpeed + Math.random() * 60 + (isSuper ? 40 : 0);
    content = content.replace(
        """function spawnChancla() {
                const isSuper = superEnabled && Math.random() < 0.18;
                const w = isSuper ? 46 : 32;
                const h = isSuper ? 26 : 18;
                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;
                const vy = baseSpeed + Math.random() * 60 + (isSuper ? 40 : 0);
                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;
                chanclas.push({ x, y, vx, vy, w, h, type: isSuper ? 'super' : 'normal', rotation: 0, rotSpeed });
                if (isSuper) sayPlayer('super');
            }""",
        """function spawnChancla() {
                const isSuper = superEnabled && Math.random() < 0.18;
                let isFire = false;

                if (isa.enraged && Math.random() < 0.25) {
                    isFire = true;
                }

                const w = isSuper ? 46 : 32;
                const h = isSuper ? 26 : 18;
                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;

                let vy = baseSpeed + Math.random() * 60 + (isSuper ? 40 : 0);
                if (isa.enraged) vy *= 1.3; // 30% faster in rage phase

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isFire) type = 'fire';
                else if (isSuper) type = 'super';

                chanclas.push({ x, y, vx, vy, w, h, type: type, rotation: 0, rotSpeed });
                if (isSuper) sayPlayer('super');
            }"""
    )

    # Also adjust spawn interval in update()
    # spawnInterval = Math.max(minSpawnInterval, spawnInterval - dt * 0.02);
    content = content.replace(
        "spawnInterval = Math.max(minSpawnInterval, spawnInterval - dt * 0.02);",
        "spawnInterval = Math.max(minSpawnInterval, spawnInterval - dt * (isa.enraged ? 0.04 : 0.02));"
    )

    # 10. Modify updateChanclas() to handle fire chancla
    # if (!c.slapped && rectsOverlap(player, c)) {
    #     if (player.shield) {
    #         player.shield = false;
    #         chanclas.splice(i, 1);
    #         continue;
    #     }
    #     const dmg = c.type === 'super' ? 2 : 1;
    #     comboCount = 0;
    #     triggerShake(c.type === 'super' ? 15 : 8, 0.4);
    content = content.replace(
        """if (!c.slapped && rectsOverlap(player, c)) {
                        if (player.shield) {
                            player.shield = false;
                            chanclas.splice(i, 1);
                            continue;
                        }
                        const dmg = c.type === 'super' ? 2 : 1;
                        comboCount = 0;
                        triggerShake(c.type === 'super' ? 15 : 8, 0.4);""",
        """if (!c.slapped && rectsOverlap(player, c)) {
                        if (player.shield) {
                            player.shield = false;
                            chanclas.splice(i, 1);
                            continue;
                        }
                        const dmg = (c.type === 'super' || c.type === 'fire') ? 2 : 1;
                        comboCount = 0;
                        triggerShake(c.type === 'super' ? 15 : (c.type === 'fire' ? 20 : 8), 0.4);"""
    )

    # 11. Modify drawChancla() to handle fire chancla
    # function drawChancla(ctx, x, y, w, h, isSuper, rotation) {
    #     ctx.save();
    #     ctx.translate(x, y);
    #
    #     // Use the thong sandal emoji for the classic "Chancla" look
    #     const emoji = isSuper ? '🩴💥' : '🩴💨';
    content = content.replace(
        "const emoji = isSuper ? '🩴💥' : '🩴💨';",
        "const emoji = isSuper ? '🩴💥' : '🩴💨'; // Default\n                // Type is no longer just boolean in some places but drawChanclaall passes c.type === 'super', we need to fix this."
    )

    # Need to fix drawChanclasAll to pass the type or change drawChancla signature
    # function drawChancla(ctx, x, y, w, h, isSuper, rotation)
    # let's change drawChancla(ctx, x, y, w, h, type, rotation)
    content = content.replace(
        "function drawChancla(ctx, x, y, w, h, isSuper, rotation) {",
        "function drawChancla(ctx, x, y, w, h, type, rotation) {"
    )
    content = content.replace(
        "const emoji = isSuper ? '🩴💥' : '🩴💨'; // Default\n                // Type is no longer just boolean in some places but drawChanclaall passes c.type === 'super', we need to fix this.",
        "let emoji = '🩴💨';\n                if (type === 'super') emoji = '🩴💥';\n                else if (type === 'fire') emoji = '🔥';"
    )
    content = content.replace(
        "const emoji = isSuper ? '🩴💥' : '🩴💨';", # in case the previous replace failed
        "let emoji = '🩴💨';\n                if (type === 'super') emoji = '🩴💥';\n                else if (type === 'fire') emoji = '🔥';"
    )
    content = content.replace(
        "function drawChanclasAll() {\n                for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type === 'super', c.rotation);\n            }",
        "function drawChanclasAll() {\n                for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation);\n            }"
    )

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
