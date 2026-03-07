import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_draw_player = "drawPlayerAvatar(ctx, x, y, Math.min(w, h), specialAttackBar >= maxSpecialAttack, expression);"
    new_draw_player = """if (player.dashTimer > 0) ctx.globalAlpha = 0.5;
                drawPlayerAvatar(ctx, x, y, Math.min(w, h), specialAttackBar >= maxSpecialAttack, expression);
                ctx.globalAlpha = 1.0;"""

    if old_draw_player in content:
        content = content.replace(old_draw_player, new_draw_player, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Done")
