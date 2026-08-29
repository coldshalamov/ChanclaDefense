import os

files = ['index.html', 'chancla_bomb.html']
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Booleans
    content = content.replace(
        "const isBoomerang = !isBomb && !isHoming && !isSuper && !isGolden && Math.random() < 0.15;",
        "const isBoomerang = !isBomb && !isHoming && !isSuper && !isGolden && Math.random() < 0.15;\n                const isTrick = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isFire && Math.random() < 0.10;"
    )

    # Dimensions
    content = content.replace(
        "else if (isGolden) { w = 36; h = 20; }",
        "else if (isGolden) { w = 36; h = 20; }\n                else if (isTrick) { w = 36; h = 36; }"
    )

    # Type
    content = content.replace(
        "else if (isGolden) type = 'golden';",
        "else if (isGolden) type = 'golden';\n                else if (isTrick) type = 'trick';"
    )

    # push statement
    content = content.replace(
        "chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed });",
        "chanclas.push({ x, y, vx, vy, vx_saved: vx, vy_saved: vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0, dodged: false, returning: false, invisible: false });"
    )

    with open(filepath, 'w') as f:
        f.write(content)
