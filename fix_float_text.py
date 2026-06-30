def fix_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Update addFloatText definition to accept and store color and fontSize
    search_add = "function addFloatText(text, x, y) {\n                floatTexts.push({ text, x, y, time: 1.8, max: 1.8 });"
    replace_add = "function addFloatText(text, x, y, color = '#fff', fontSize = 14) {\n                floatTexts.push({ text, x, y, time: 1.8, max: 1.8, color, fontSize });"
    content = content.replace(search_add, replace_add)

    # Update drawFloatTexts to use color and fontSize
    search_draw = """            function drawFloatTexts() {
                floatTexts.forEach(f => {
                    ctx.save();
                    ctx.globalAlpha = Math.max(0, f.time / f.max);
                    ctx.fillStyle = '#fff';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.textAlign = 'center';"""
    replace_draw = """            function drawFloatTexts() {
                floatTexts.forEach(f => {
                    ctx.save();
                    ctx.globalAlpha = Math.max(0, f.time / f.max);
                    ctx.fillStyle = f.color || '#fff';
                    ctx.font = `bold ${f.fontSize || 16}px sans-serif`;
                    ctx.textAlign = 'center';
                    // add black outline for visibility
                    ctx.strokeStyle = '#000';
                    ctx.lineWidth = 3;
                    ctx.strokeText(f.text, f.x, f.y);"""
    content = content.replace(search_draw, replace_draw)

    with open(filename, 'w') as f:
        f.write(content)

fix_file('index.html')
fix_file('chancla_bomb.html')
