import sys

with open("index.html", "r") as f:
    content = f.read()

# 1. Add spawnChanclaSpread() after spawnChancla()
old_spawn_chancla_end = "if (isSuper) sayPlayer('super');\n            }"
new_spawn_chancla_end = """if (isSuper) sayPlayer('super');
            }

            function spawnChanclaSpread() {
                const vxs = [-100, 0, 100];
                for(let i=0; i<3; i++) {
                    const isSuper = superEnabled && Math.random() < 0.18;
                    const w = isSuper ? 46 : 32;
                    const h = isSuper ? 26 : 18;
                    const x = canvas.width/2;
                    const y = isa.y + 40;
                    const vy = baseSpeed + Math.random() * 60 + (isSuper ? 40 : 0);
                    const vx = vxs[i];
                    const rotSpeed = (Math.random() - 0.5) * 5;
                    chanclas.push({ x, y, vx, vy, w, h, type: isSuper ? 'super' : 'normal', rotation: 0, rotSpeed });
                }
                if(superEnabled) sayPlayer('super');
            }"""
if old_spawn_chancla_end in content:
    content = content.replace(old_spawn_chancla_end, new_spawn_chancla_end, 1)
else:
    print("Failed to find spawnChancla() end")

# 2. Update spawn logic in update(dt)
old_spawn_logic = """if (spawnTimer >= spawnInterval && isa.chismeTimer <= 0) {
                    spawnChancla();
                    spawnTimer = 0;
                }"""
new_spawn_logic = """if (spawnTimer >= spawnInterval && isa.chismeTimer <= 0) {
                    if (isa.isEnraged && Math.random() < 0.25) spawnChanclaSpread();
                    else spawnChancla();
                    spawnTimer = 0;
                }"""
if old_spawn_logic in content:
    content = content.replace(old_spawn_logic, new_spawn_logic, 1)
else:
    print("Failed to find spawn logic")

with open("index.html", "w") as f:
    f.write(content)

print("Patch 2 applied.")
