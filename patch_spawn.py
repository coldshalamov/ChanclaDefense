def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_spawn = """            function spawnChancla() {
                const isSuper = superEnabled && Math.random() < 0.18;
                const w = isSuper ? 46 : 32;
                const h = isSuper ? 26 : 18;
                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;
                const vy = baseSpeed + Math.random() * 60 + (isSuper ? 40 : 0);
                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;
                chanclas.push({ x, y, vx, vy, w, h, type: isSuper ? 'super' : 'normal', rotation: 0, rotSpeed });
                if (isSuper) sayPlayer('super');
            }"""

    new_spawn = """            function spawnChancla() {
                const isSuper = superEnabled && Math.random() < 0.18;
                const isGolden = !isSuper && timeElapsed > 25 && Math.random() < 0.05;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isGolden) { w = 38; h = 22; } // slightly bigger than normal

                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;
                const vy = baseSpeed + Math.random() * 60 + (isSuper ? 40 : (isGolden ? 80 : 0));
                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;
                chanclas.push({ x, y, vx, vy, w, h, type: isSuper ? 'super' : (isGolden ? 'golden' : 'normal'), rotation: 0, rotSpeed });
                if (isSuper) sayPlayer('super');
            }"""

    content = content.replace(old_spawn, new_spawn, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
