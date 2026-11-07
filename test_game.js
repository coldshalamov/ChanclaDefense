const fs = require('fs');
const content = fs.readFileSync('index.html', 'utf8');

if (content.includes('let dashCooldown = 0;')) {
    console.log("dashCooldown is declared");
} else {
    console.log("dashCooldown is NOT declared");
}
