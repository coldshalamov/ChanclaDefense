import sys

with open("index.html", "r") as f:
    content = f.read()

# 1. Update isa object initialization
old_isa_init = "const isa = { x: canvas.width / 2, y: 70, anger: 100, maxAnger: 100, hitTimer: 0, chismeTimer: 0 };"
new_isa_init = "const isa = { x: canvas.width / 2, y: 70, anger: 100, maxAnger: 100, hitTimer: 0, chismeTimer: 0, isEnraged: false };"
if old_isa_init in content:
    content = content.replace(old_isa_init, new_isa_init, 1)
else:
    print("Failed to find isa init")

# 2. Update resetGame()
old_reset_game = "isa.chismeTimer = 0;"
new_reset_game = "isa.chismeTimer = 0;\n                isa.isEnraged = false;"
if old_reset_game in content:
    content = content.replace(old_reset_game, new_reset_game, 1)
else:
    print("Failed to find resetGame")

# 3. Add logic in update(dt) before timeElapsed += dt;
old_update_logic = "timeElapsed += dt;"
new_update_logic = """if (isa.anger <= isa.maxAnger * 0.5 && !isa.isEnraged) {
                    isa.isEnraged = true;
                    addFloatText("RAGE MODE!", canvas.width / 2, canvas.height / 2);
                    shakeTimer = 0.5;
                    shakeIntensity = 10;
                    playSound(300, 0.5);
                    baseSpeed += 40;
                    spawnInterval *= 0.75;
                }
                timeElapsed += dt;"""
if old_update_logic in content:
    content = content.replace(old_update_logic, new_update_logic, 1)
else:
    print("Failed to find update logic")

with open("index.html", "w") as f:
    f.write(content)

print("Patch 1 applied.")
