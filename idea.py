with open("index.html", "r") as f:
    content = f.read()

# Replace spawnChancla
import re
new_spawn = """            function spawnChancla() {
                const isBomb = Math.random() < 0.08;
                const isGhost = !isBomb && Math.random() < 0.12;
                const isHoming = superEnabled && !isBomb && !isGhost && Math.random() < 0.10;
                const isSuper = superEnabled && !isBomb && !isGhost && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isGhost && !isHoming && !isSuper && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }
                else if (isGhost) { w = 34; h = 34; }

                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;

                let vy = baseSpeed + Math.random() * 60;
                if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed
                else if (isGhost) vy = baseSpeed * 0.85;

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';
                else if (isGhost) type = 'ghost';

                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, invisible: false });
                if (isSuper) sayPlayer('super');
            }"""

content = re.sub(r'function spawnChancla\(\) \{.*?\n            \}\n', new_spawn + '\n\n', content, flags=re.DOTALL)
with open("test.html", "w") as f:
    f.write(content)
