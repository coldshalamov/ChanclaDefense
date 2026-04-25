import re

def patch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Variables
    content = re.sub(r'\s*let pets = \[\];\n\s*let powerups = \[\];', '', content)
    content = re.sub(r'\s*const slowEffect = \{ timer: 0, factor: 0\.62 \};', '', content)

    # Dialogue
    content = re.sub(r'\s*petOwen: \[\s*[^\]]+?\s*\],', '', content)

    # resetGame
    content = re.sub(r'\s*pets = \[\];\n\s*powerups = \[\];', '', content)
    content = re.sub(r'\s*slowEffect\.timer = 0;', '', content)

    # drawPlayer expressions
    content = re.sub(r'\s*else if \(slowEffect\.timer > 0\) expression = \'chill\';', '', content)

    # drawPlayerAvatar expressions
    content = re.sub(r'\s*\} else if \(expression === \'chill\'\) \{\s*ctx\.rotate\(Math\.sin\(timeElapsed \* 3\) \* 0\.08\);\s*// Relaxed sway', '', content)
    content = re.sub(r'\s*if \(expression === \'chill\'\) \{\s*ctx\.fillStyle = \'#111\';\s*ctx\.fill\(\);\s*\}', '', content)

    eyes_chill_regex = r'\s*if \(expression === \'chill\'\) \{\s*// Reflection on sunglasses\s*ctx\.fillStyle = \'rgba\(255,255,255,0\.3\)\';\s*ctx\.beginPath\(\);\s*ctx\.moveTo\(-headW \* 0\.28, -headH \* 0\.08\);\s*ctx\.lineTo\(-headW \* 0\.18, -headH \* 0\.08\);\s*ctx\.lineTo\(-headW \* 0\.28, 0\);\s*ctx\.fill\(\);\s*ctx\.beginPath\(\);\s*ctx\.moveTo\(headW \* 0\.12, -headH \* 0\.08\);\s*ctx\.lineTo\(headW \* 0\.22, -headH \* 0\.08\);\s*ctx\.lineTo\(headW \* 0\.12, 0\);\s*ctx\.fill\(\);\s*\} else if \(expression === \'hit\'\) \{'
    content = re.sub(eyes_chill_regex, r'\n                if (expression === \'hit\') {', content)

    mouth_chill_regex = r'\s*\} else if \(expression === \'chill\'\) \{\s*// Cool smirk\s*ctx\.strokeStyle = \'#1e130c\';\s*ctx\.lineWidth = 1\.6;\s*ctx\.beginPath\(\);\s*ctx\.moveTo\(-headW \* 0\.1, headH \* 0\.24\);\s*ctx\.quadraticCurveTo\(0, headH \* 0\.26, headW \* 0\.12, headH \* 0\.22\);\s*ctx\.stroke\(\);'
    content = re.sub(mouth_chill_regex, '', content)

    # HUD chill timer
    hud_regex = r'\s*if \(slowEffect\.timer > 0\) \{\s*ctx\.fillStyle = \'#ffd166\';\s*ctx\.font = \'14px sans-serif\';\s*ctx\.textAlign = \'center\';\s*ctx\.fillText\(\'🍺 chill \' \+ slowEffect\.timer\.toFixed\(1\) \+ \'s\', canvas\.width / 2, 22\);\s*\}'
    content = re.sub(hud_regex, '', content)

    # updateChanclas slowFactor
    content = re.sub(r'\s*const slowFactor = slowEffect\.timer > 0 \? slowEffect\.factor : 1;', '', content)
    content = content.replace(r'c.y += c.vy * dt * (c.slapped ? 1 : slowFactor);', r'c.y += c.vy * dt;')

    # update calls
    content = re.sub(r'\s*if \(!pets\.some\(p => p\.kind === \'owen\'\) && \(player\.lives <= 2 && Math\.random\(\) < 0\.003 \|\| Math\.random\(\) < 0\.0007\)\) \{\s*spawnOwen\(\);\s*\}', '', content)
    content = re.sub(r'\s*updatePets\(dt\);\n\s*updatePowerups\(dt\);', r'\n                updateFloatTexts(dt);', content)
    content = re.sub(r'\s*if \(slowEffect\.timer > 0\) slowEffect\.timer -= dt;', '', content)

    # draw calls
    content = re.sub(r'\s*drawPowerups\(\);\n\s*drawSpecialProjectiles\(\);\n\s*drawPets\(\);', r'\n                drawSpecialProjectiles();', content)

    # Functions
    draw_pets_regex = r'\s*function drawPets\(\) \{[\s\S]*?\}\s*function drawOwen\(p\) \{[\s\S]*?\}'
    content = re.sub(draw_pets_regex, '', content)

    spawn_owen_regex = r'\s*function spawnOwen\(\) \{[\s\S]*?\}'
    content = re.sub(spawn_owen_regex, '', content)

    spawn_powerup_regex = r'\s*function spawnPowerup\(kind, x, y\) \{[\s\S]*?\}'
    content = re.sub(spawn_powerup_regex, '', content)

    apply_powerup_regex = r'\s*function applyPowerup\(p\) \{[\s\S]*?\}'
    content = re.sub(apply_powerup_regex, '', content)

    update_pets_regex = r'\s*function updatePets\(dt\) \{[\s\S]*?continue;\s*\}\s*\}\s*\}\s*\}'
    content = re.sub(update_pets_regex, '', content)

    draw_powerups_regex = r'\s*function drawPowerups\(\) \{[\s\S]*?\}\s*\);\s*\}'
    content = re.sub(draw_powerups_regex, '', content)

    update_powerups_regex = r'\s*function updatePowerups\(dt\) \{[\s\S]*?powerups\.splice\(i, 1\);\s*\}\s*\}'
    update_float_texts = r'\n            function updateFloatTexts(dt) {'
    content = re.sub(update_powerups_regex, update_float_texts, content)


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch('index.html')
patch('chancla_bomb.html')
