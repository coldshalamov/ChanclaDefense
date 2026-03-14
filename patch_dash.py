import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. player object
    content = content.replace(
        "const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0 };",
        "const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0, dashTimer: 0, dashCooldown: 0, dashDir: 0 };"
    )

    # 2. resetGame
    content = content.replace(
        "player.hitTimer = 0;\n                isa.anger = isa.maxAnger;",
        "player.hitTimer = 0;\n                player.dashTimer = 0;\n                player.dashCooldown = 0;\n                player.dashDir = 0;\n                isa.anger = isa.maxAnger;"
    )

    # 3. keys and touch
    content = content.replace(
        "const keys = { left: false, right: false };\n            const touch = { left: false, right: false };",
        "const keys = { left: false, right: false };\n            const touch = { left: false, right: false };\n            const lastTap = { left: 0, right: 0 };"
    )

    # 4. drawPlayer
    content = content.replace(
        "function drawPlayer() {\n                const { x, y, w, h } = player;\n                ctx.save();\n                ctx.fillStyle = '#fff';",
        "function drawPlayer() {\n                const { x, y, w, h } = player;\n                ctx.save();\n                if (player.dashTimer > 0) {\n                    ctx.globalAlpha = 0.5;\n                }\n                ctx.fillStyle = '#fff';"
    )

    # 5. updateChanclas
    content = content.replace(
        "if (!c.slapped && rectsOverlap(player, c)) {\n                        if (player.shield) {",
        "if (!c.slapped && rectsOverlap(player, c)) {\n                        if (player.hitTimer > 0 || player.dashTimer > 0) continue;\n                        if (player.shield) {"
    )

    # 6. update(dt) movement
    content = content.replace(
        "const speed = player.speed;\n                const moveLeft = keys.left || touch.left;\n                const moveRight = keys.right || touch.right;\n                if (moveLeft) player.x -= speed * dt;\n                if (moveRight) player.x += speed * dt;\n                player.x = Math.max(player.w / 2 + 10, Math.min(canvas.width - player.w / 2 - 10, player.x));",
        "const speed = player.speed;\n                if (player.dashTimer > 0) {\n                    player.x += speed * 2.5 * player.dashDir * dt;\n                    if (Math.random() < 0.4) {\n                        rosePetals.push({\n                            x: player.x,\n                            y: player.y - 10,\n                            vx: (Math.random() - 0.5) * 50,\n                            vy: -10 - Math.random() * 20,\n                            rotation: Math.random() * Math.PI * 2,\n                            rotSpeed: (Math.random() - 0.5) * 5,\n                            emoji: '💨',\n                            size: 20\n                        });\n                    }\n                } else {\n                    const moveLeft = keys.left || touch.left;\n                    const moveRight = keys.right || touch.right;\n                    if (moveLeft) player.x -= speed * dt;\n                    if (moveRight) player.x += speed * dt;\n                }\n                player.x = Math.max(player.w / 2 + 10, Math.min(canvas.width - player.w / 2 - 10, player.x));"
    )

    # 7. update(dt) decrement timers
    content = content.replace(
        "if (player.hitTimer > 0) player.hitTimer -= dt;\n                if (isa.chismeTimer > 0) isa.chismeTimer -= dt;\n\n                if (dialogueTimer > 0) dialogueTimer -= dt;",
        "if (player.hitTimer > 0) player.hitTimer -= dt;\n                if (isa.chismeTimer > 0) isa.chismeTimer -= dt;\n                if (player.dashTimer > 0) player.dashTimer -= dt;\n                if (player.dashCooldown > 0) player.dashCooldown -= dt;\n\n                if (dialogueTimer > 0) dialogueTimer -= dt;"
    )

    # 8. handleMobileZones
    content = content.replace(
        "function handleMobileZones(zone, dir) {\n                zone.addEventListener('touchstart', (e) => {\n                    if (state !== STATE.PLAYING) return;\n                    touch[dir] = true;\n                    e.preventDefault();\n                }, { passive: false });",
        "function handleMobileZones(zone, dir) {\n                zone.addEventListener('touchstart', (e) => {\n                    if (state !== STATE.PLAYING) return;\n                    if (player.dashCooldown <= 0) {\n                        const now = Date.now();\n                        if (now - lastTap[dir] < 300) {\n                            player.dashTimer = 0.25;\n                            player.dashCooldown = 0.8;\n                            player.dashDir = dir === 'left' ? -1 : 1;\n                        }\n                        lastTap[dir] = now;\n                    }\n                    touch[dir] = true;\n                    e.preventDefault();\n                }, { passive: false });"
    )

    # 9. handleKey
    content = content.replace(
        "function handleKey(e, isDown) {\n                if (['ArrowLeft', 'a', 'A'].includes(e.key)) { keys.left = isDown; e.preventDefault(); }\n                if (['ArrowRight', 'd', 'D'].includes(e.key)) { keys.right = isDown; e.preventDefault(); }",
        "function handleKey(e, isDown) {\n                if (['ArrowLeft', 'a', 'A'].includes(e.key)) {\n                    if (isDown && !keys.left && state === STATE.PLAYING && player.dashCooldown <= 0) {\n                        const now = Date.now();\n                        if (now - lastTap.left < 300) {\n                            player.dashTimer = 0.25;\n                            player.dashCooldown = 0.8;\n                            player.dashDir = -1;\n                        }\n                        lastTap.left = now;\n                    }\n                    keys.left = isDown; e.preventDefault();\n                }\n                if (['ArrowRight', 'd', 'D'].includes(e.key)) {\n                    if (isDown && !keys.right && state === STATE.PLAYING && player.dashCooldown <= 0) {\n                        const now = Date.now();\n                        if (now - lastTap.right < 300) {\n                            player.dashTimer = 0.25;\n                            player.dashCooldown = 0.8;\n                            player.dashDir = 1;\n                        }\n                        lastTap.right = now;\n                    }\n                    keys.right = isDown; e.preventDefault();\n                }"
    )

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Patched {filepath}")

patch_file('index.html')
patch_file('chancla_bomb.html')
