import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update drawChancla signature and body
    old_draw = """            function drawChancla(ctx, x, y, w, h, isSuper, rotation) {
                ctx.save();
                ctx.translate(x, y);

                // Use the thong sandal emoji for the classic "Chancla" look
                const emoji = isSuper ? '🩴💥' : '🩴💨';

                // Prioritize Noto Color Emoji and system emoji fonts
                ctx.font = `${Math.max(28, w * 1.4)}px 'Noto Color Emoji', 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif`;
                ctx.textAlign = 'center';
                ctx.rotate(rotation);
                ctx.fillText(emoji, 0, h * 0.2);
                ctx.restore();
            }"""

    new_draw = """            function drawChancla(ctx, x, y, w, h, type, rotation) {
                ctx.save();
                ctx.translate(x, y);

                // Use the thong sandal emoji for the classic "Chancla" look
                let emoji = '🩴💨';
                if (type === 'super') emoji = '🩴💥';
                else if (type === 'golden') emoji = '🩴✨';

                // Prioritize Noto Color Emoji and system emoji fonts
                ctx.font = `${Math.max(28, w * 1.4)}px 'Noto Color Emoji', 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif`;
                ctx.textAlign = 'center';
                ctx.rotate(rotation);

                if (type === 'golden') {
                    ctx.shadowColor = 'gold';
                    ctx.shadowBlur = 10;
                }

                ctx.fillText(emoji, 0, h * 0.2);
                ctx.restore();
            }"""

    content = content.replace(old_draw, new_draw, 1)

    # 2. Update drawChanclasAll
    old_draw_all = """            function drawChanclasAll() {
                for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type === 'super', c.rotation);
            }"""

    new_draw_all = """            function drawChanclasAll() {
                for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation);
            }"""

    content = content.replace(old_draw_all, new_draw_all, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
