import re

with open('index.html', 'r') as f:
    content = f.read()

# Update player speed calculation in `update`
speed_old = "const speed = player.speed;"
speed_new = "const speed = player.chiliTimer > 0 ? player.speed * 1.2 : player.speed;"
content = content.replace(speed_old, speed_new, 1)

# Update trySlap logic for perfect slap
try_slap_old = "const isPerfect = dist < perfectRange;"
try_slap_new = "const isPerfect = (dist < perfectRange) || (player.chiliTimer > 0);"
content = content.replace(try_slap_old, try_slap_new, 1)

# Update updateChanclas to check for chiliTimer collision and hitTimer i-frames
update_chanclas_old = """                    if (!c.slapped && rectsOverlap(player, c)) {
                        if (player.shield) {"""

update_chanclas_new = """                    if (!c.slapped && rectsOverlap(player, c)) {
                        if (player.chiliTimer > 0) {
                            spawnImpact(c.x, c.y);
                            score += 5;
                            comboCount++;
                            chanclas.splice(i, 1);
                            playSound(600, 0.1);
                            continue;
                        }
                        if (player.hitTimer > 0) continue;
                        if (player.shield) {"""

content = content.replace(update_chanclas_old, update_chanclas_new, 1)

# Add chiliTimer decrement in `update`
timer_dec_old = "if (slowEffect.timer > 0) slowEffect.timer -= dt;"
timer_dec_new = "if (player.chiliTimer > 0) player.chiliTimer -= dt;\n                if (slowEffect.timer > 0) slowEffect.timer -= dt;"
content = content.replace(timer_dec_old, timer_dec_new, 1)

with open('index.html', 'w') as f:
    f.write(content)
