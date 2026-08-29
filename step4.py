import os
files = ['index.html', 'chancla_bomb.html']
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace("else if (type === 'golden') emoji = '✨👞';", "else if (type === 'golden') emoji = '✨👞';\n                else if (type === 'trick') emoji = '🃏';")

    shadow_replace = """                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    } else if (type === 'trick') {
                        ctx.shadowColor = '#ff00ff';
                        ctx.shadowBlur = 15;
                    } else if (type === 'golden') {"""

    original_shadow = """                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    } else if (type === 'golden') {"""

    content = content.replace(original_shadow, shadow_replace)

    with open(filepath, 'w') as f:
        f.write(content)
