import sys

with open("index.html", "r") as f:
    content = f.read()

# 1. Update drawBackground()
old_bg_grad = """grad.addColorStop(0, '#0b1930');
                grad.addColorStop(1, '#0f243a');"""
new_bg_grad = """grad.addColorStop(0, isa.isEnraged ? '#300b0b' : '#0b1930');
                grad.addColorStop(1, isa.isEnraged ? '#3a0f0f' : '#0f243a');"""
if old_bg_grad in content:
    content = content.replace(old_bg_grad, new_bg_grad, 1)
else:
    print("Failed to find drawBackground grad")

# 2. Update drawIsa()
old_draw_isa = "drawIsaAvatar(ctx, drawX, drawY, 78, isa.hitTimer > 0);"
new_draw_isa = """if(isa.isEnraged) {
                    ctx.shadowColor = '#ff0000';
                    ctx.shadowBlur = 20 + Math.sin(timeElapsed * 10) * 10;
                }
                drawIsaAvatar(ctx, drawX, drawY, 78, isa.hitTimer > 0, isa.isEnraged);
                ctx.shadowBlur = 0;
                ctx.shadowColor = 'transparent';"""
if old_draw_isa in content:
    content = content.replace(old_draw_isa, new_draw_isa, 1)
else:
    print("Failed to find drawIsa avatar call")

# 3. Update drawIsaAvatar() signature and eyes
old_avatar_sig = "function drawIsaAvatar(ctx, x, y, size, isHit) {"
new_avatar_sig = "function drawIsaAvatar(ctx, x, y, size, isHit, isEnraged) {"
if old_avatar_sig in content:
    content = content.replace(old_avatar_sig, new_avatar_sig, 1)
else:
    print("Failed to find drawIsaAvatar sig")

old_avatar_eyes = """} else {
                    // Normal eyes with lashes
                    ctx.fillStyle = '#1d1411';"""
new_avatar_eyes = """} else if (isEnraged) {
                    ctx.fillStyle = '#ff0000';
                    ctx.beginPath();
                    ctx.arc(-faceW * 0.2, -faceH * 0.05, faceW * 0.08, 0, Math.PI * 2);
                    ctx.arc(faceW * 0.2, -faceH * 0.05, faceW * 0.08, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = '#1d1411';
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.moveTo(-faceW * 0.3, -faceH * 0.12);
                    ctx.lineTo(-faceW * 0.1, -faceH * 0.08);
                    ctx.moveTo(faceW * 0.3, -faceH * 0.12);
                    ctx.lineTo(faceW * 0.1, -faceH * 0.08);
                    ctx.stroke();
                } else {
                    // Normal eyes with lashes
                    ctx.fillStyle = '#1d1411';"""
if old_avatar_eyes in content:
    content = content.replace(old_avatar_eyes, new_avatar_eyes, 1)
else:
    print("Failed to find drawIsaAvatar eyes logic")

with open("index.html", "w") as f:
    f.write(content)

print("Patch 3 applied.")
