import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Patch 1: Extend background box in drawTitleScreen
    old_rect = "roundRect(ctx, 30, 260, canvas.width - 60, 200, 16);"
    new_rect = "roundRect(ctx, 30, 260, canvas.width - 60, 260, 16);"
    if old_rect in content:
        content = content.replace(old_rect, new_rect, 1)

    # Patch 2: Add Achievements button
    old_shop_btn = """                // Shop Button
                ctx.fillStyle = '#2196f3';
                roundRect(ctx, 110, 450, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Shop / Tienda', canvas.width / 2, 480);"""

    new_shop_btn = """                // Shop Button
                ctx.fillStyle = '#2196f3';
                roundRect(ctx, 110, 450, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Shop / Tienda', canvas.width / 2, 480);

                // Achievements Button
                ctx.fillStyle = '#9b59b6';
                roundRect(ctx, 110, 520, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Logros / Medals', canvas.width / 2, 550);"""

    if old_shop_btn in content:
        content = content.replace(old_shop_btn, new_shop_btn, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('chancla_bomb.html')
