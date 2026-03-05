import re

with open('index.html', 'r') as f:
    content = f.read()

# Update drawPowerups
powerup_old = """} else if (p.kind === 'taco') {
                        ctx.font = '30px "Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('🌮', 0, 0);"""
powerup_new = """} else if (p.kind === 'chili') {
                        ctx.font = '30px "Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('🌶️', 0, 0);"""
content = content.replace(powerup_old, powerup_new, 1)

# Update drawPlayer
draw_player_old = """                else if (slapEffect.timer > 0) expression = 'slap';
                else if (slowEffect.timer > 0) expression = 'chill';
                else if (comboCount >= 5) expression = 'cocky';"""
draw_player_new = """                else if (slapEffect.timer > 0) expression = 'slap';
                else if (player.chiliTimer > 0) expression = 'spicy';
                else if (slowEffect.timer > 0) expression = 'chill';
                else if (comboCount >= 5) expression = 'cocky';"""
content = content.replace(draw_player_old, draw_player_new, 1)

draw_player_aura_old = """                drawPlayerAvatar(ctx, x, y, Math.min(w, h), specialAttackBar >= maxSpecialAttack, expression);"""
draw_player_aura_new = """                drawPlayerAvatar(ctx, x, y, Math.min(w, h), specialAttackBar >= maxSpecialAttack, expression);
                if (player.chiliTimer > 0) {
                    ctx.strokeStyle = '#ff4500';
                    ctx.lineWidth = 4;
                    ctx.beginPath();
                    ctx.arc(x, y, w * 0.8, 0, Math.PI * 2);
                    ctx.stroke();
                }"""
content = content.replace(draw_player_aura_old, draw_player_aura_new, 1)

# Update drawPlayerAvatar
avatar_shake_old = """                if (expression === 'hit') {
                    ctx.rotate((Math.random() - 0.5) * 0.25);
                } else if (expression === 'chill') {"""
avatar_shake_new = """                if (expression === 'hit') {
                    ctx.rotate((Math.random() - 0.5) * 0.25);
                } else if (expression === 'spicy') {
                    ctx.rotate((Math.random() - 0.5) * 0.1);
                } else if (expression === 'chill') {"""
content = content.replace(avatar_shake_old, avatar_shake_new, 1)

avatar_eyes_old = """                } else if (expression === 'cocky') {
                    // Confident eyes with eyebrow raise
                    ctx.fillStyle = '#2a1b12';"""
avatar_eyes_new = """                } else if (expression === 'spicy') {
                    // Fiery eyes
                    ctx.fillStyle = '#ff4500';
                    ctx.beginPath();
                    ctx.arc(-headW * 0.2, -headH * 0.03, headW * 0.055, 0, Math.PI * 2);
                    ctx.arc(headW * 0.2, -headH * 0.03, headW * 0.055, 0, Math.PI * 2);
                    ctx.fill();
                    // Eyebrows
                    ctx.strokeStyle = '#2f1d12';
                    ctx.lineWidth = 2.5;
                    ctx.beginPath();
                    ctx.moveTo(-headW * 0.28, -headH * 0.15);
                    ctx.lineTo(-headW * 0.12, -headH * 0.06);
                    ctx.moveTo(headW * 0.28, -headH * 0.15);
                    ctx.lineTo(headW * 0.12, -headH * 0.06);
                    ctx.stroke();
                } else if (expression === 'cocky') {
                    // Confident eyes with eyebrow raise
                    ctx.fillStyle = '#2a1b12';"""
content = content.replace(avatar_eyes_old, avatar_eyes_new, 1)

avatar_mouth_old = """                } else if (expression === 'chill') {
                    // Cool smirk
                    ctx.strokeStyle = '#1e130c';"""
avatar_mouth_new = """                } else if (expression === 'spicy') {
                    // Angry open mouth
                    ctx.fillStyle = '#4a2c22';
                    ctx.beginPath();
                    ctx.ellipse(0, headH * 0.24, headW * 0.1, headH * 0.06, 0, 0, Math.PI * 2);
                    ctx.fill();
                } else if (expression === 'chill') {
                    // Cool smirk
                    ctx.strokeStyle = '#1e130c';"""
content = content.replace(avatar_mouth_old, avatar_mouth_new, 1)

# Update drawHUD
hud_old = """                if (slowEffect.timer > 0) {
                    ctx.fillStyle = '#ffd166';
                    ctx.font = '14px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('🍺 chill ' + slowEffect.timer.toFixed(1) + 's', canvas.width / 2, 22);
                }"""
hud_new = """                if (slowEffect.timer > 0) {
                    ctx.fillStyle = '#ffd166';
                    ctx.font = '14px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('🍺 chill ' + slowEffect.timer.toFixed(1) + 's', canvas.width / 2, 22);
                } else if (player.chiliTimer > 0) {
                    ctx.fillStyle = '#ff4500';
                    ctx.font = '14px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('🌶️ spicy ' + player.chiliTimer.toFixed(1) + 's', canvas.width / 2, 22);
                }"""
content = content.replace(hud_old, hud_new, 1)

with open('index.html', 'w') as f:
    f.write(content)
