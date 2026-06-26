import os

def check_content(filename):
    with open(filename, 'r') as f:
        return f.read()

for filename in ['index.html', 'chancla_bomb.html']:
    content = check_content(filename)
    assert 'let hitStop = 0;' in content
    assert 'hitStop = 0;' in content
    assert 'function update(dt) {\n                if (state !== STATE.PLAYING) return;\n\n                if (shakeTimer > 0) {' in content
    assert 'ctx.fillStyle = grad;\n                ctx.fillRect(0, 0, canvas.width, canvas.height);' in content
    assert 'if (dashTimer > 0) continue; // I-frames during dash' in content
    assert 'if (dashTimer > 0) continue; // I-frames during dash shockwave' in content

print("All assertions passed.")
