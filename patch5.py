import re

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The game includes a 'Ghost Chancla' mechanic where projectiles turn invisible mid-flight
    # Let's add that!

    ghost_spawn_search = """                const isTrick = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && Math.random() < 0.10;"""
    ghost_spawn_replace = """                const isTrick = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && Math.random() < 0.10;
                const isGhost = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && Math.random() < 0.15;"""

    content = content.replace(ghost_spawn_search, ghost_spawn_replace, 1)

    ghost_spawn_search2 = """                const isSniper = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && Math.random() < 0.12;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && Math.random() < 0.25;"""
    ghost_spawn_replace2 = """                const isSniper = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isGhost && Math.random() < 0.12;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isGhost && !isSniper && Math.random() < 0.25;"""
    content = content.replace(ghost_spawn_search2, ghost_spawn_replace2, 1)

    ghost_spawn_search3 = """                else if (isTrick) { w = 36; h = 22; }"""
    ghost_spawn_replace3 = """                else if (isTrick) { w = 36; h = 22; }
                else if (isGhost) { w = 32; h = 18; }"""
    content = content.replace(ghost_spawn_search3, ghost_spawn_replace3, 1)

    ghost_spawn_search4 = """                else if (isTrick) vy = baseSpeed * 0.9;"""
    ghost_spawn_replace4 = """                else if (isTrick) vy = baseSpeed * 0.9;
                else if (isGhost) vy = baseSpeed * 0.8;"""
    content = content.replace(ghost_spawn_search4, ghost_spawn_replace4, 1)

    ghost_spawn_search5 = """                else if (isTrick) type = 'trick';"""
    ghost_spawn_replace5 = """                else if (isTrick) type = 'trick';
                else if (isGhost) type = 'ghost';"""
    content = content.replace(ghost_spawn_search5, ghost_spawn_replace5, 1)

    ghost_spawn_search6 = """                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0,"""
    ghost_spawn_replace6 = """                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0, invisible: false,"""
    content = content.replace(ghost_spawn_search6, ghost_spawn_replace6, 1)

    ghost_draw_search1 = """                else if (type === 'trick') emoji = '🃏';"""
    ghost_draw_replace1 = """                else if (type === 'trick') emoji = '🃏';
                else if (type === 'ghost') emoji = '👻';"""
    content = content.replace(ghost_draw_search1, ghost_draw_replace1, 1)

    ghost_draw_search2 = """                // Prioritize Noto Color Emoji and system emoji fonts"""
    ghost_draw_replace2 = """                // Prioritize Noto Color Emoji and system emoji fonts
                if (type === 'ghost') {
                    if (y > canvas.height * 0.3 && y < canvas.height * 0.7) {
                        ctx.globalAlpha = 0.1;
                    }
                }"""
    content = content.replace(ghost_draw_search2, ghost_draw_replace2, 1)


    with open(filepath, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
