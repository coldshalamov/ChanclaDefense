const fs = require('fs');

function applyZoomPatch(filePath) {
    let code = fs.readFileSync(filePath, 'utf8');

    // Patch start of draw()
    const drawStartSearch = `            function draw() {
                drawBackground();`;
    const drawStartReplace = `            function draw() {
                ctx.save();
                if (hitStop > 0) {
                    const zoom = 1.08;
                    const cx = player.x;
                    const cy = player.y;
                    ctx.translate(cx, cy);
                    ctx.scale(zoom, zoom);
                    ctx.translate(-cx, -cy);
                }
                drawBackground();`;

    code = code.replace(drawStartSearch, drawStartReplace);

    // Patch end of draw()
    const drawEndSearch = `                drawPlayer();
                drawSlapEffect();

                drawLowHealthVignette();`;
    const drawEndReplace = `                drawPlayer();
                drawSlapEffect();
                ctx.restore();

                drawLowHealthVignette();`;

    code = code.replace(drawEndSearch, drawEndReplace);

    fs.writeFileSync(filePath, code);
    console.log("Patched " + filePath);
}

applyZoomPatch('index.html');
applyZoomPatch('chancla_bomb.html');
