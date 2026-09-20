import re

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Redefine drawChancla to include the full chancla object

    # 1. Update drawChancla signature
    search1 = "function drawChancla(ctx, x, y, w, h, type, rotation) {"
    replace1 = "function drawChancla(ctx, c, x, y, w, h, type, rotation) {"
    content = content.replace(search1, replace1, 1)

    # 2. Update drawChanclasAll loop
    search2 = "for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation);"
    replace2 = "for (const c of chanclas) drawChancla(ctx, c, c.x, c.y, c.w, c.h, c.type, c.rotation);"
    content = content.replace(search2, replace2, 1)

    # 3. Update ghost alpha logic in drawChancla
    search3 = """                if (type === 'ghost') {
                    if (y > canvas.height * 0.3 && y < canvas.height * 0.7) {
                        ctx.globalAlpha = 0.1;
                    }
                }"""
    replace3 = """                if (type === 'ghost' && c.invisible) {
                    ctx.globalAlpha = 0.1;
                }"""
    content = content.replace(search3, replace3, 1)

    with open(filepath, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
