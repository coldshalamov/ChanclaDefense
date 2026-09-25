const fs = require('fs');

function applyPerfectPatch(filePath) {
    let code = fs.readFileSync(filePath, 'utf8');

    // Add witchTime logic
    const perfectSearch = `                        c.vx = (c.x - player.x) * (isPerfect ? 12 : 8);`;
    const perfectReplace = `                        if (isPerfect) {
                            witchTimeTimer = 0.5; // Trigger bullet time
                            triggerFlash(0.1, '#cc00ff');
                            playSound(850, 0.1);
                        }
                        c.vx = (c.x - player.x) * (isPerfect ? 12 : 8);`;

    code = code.replace(perfectSearch, perfectReplace);

    fs.writeFileSync(filePath, code);
    console.log("Patched " + filePath);
}

applyPerfectPatch('index.html');
applyPerfectPatch('chancla_bomb.html');
