with open("index.html", "r") as f:
    content = f.read()

search_str = """                const isBomb = Math.random() < 0.08;
                const isHoming = superEnabled && !isBomb && Math.random() < 0.10;
                const isSuper = superEnabled && !isBomb && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }

                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;

                let vy = baseSpeed + Math.random() * 60;
                if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';

                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed });
                if (isSuper) sayPlayer('super');"""

replace_str = """                const isGolden = Math.random() < 0.05;
                const isBomb = !isGolden && Math.random() < 0.08;
                const isHoming = superEnabled && !isGolden && !isBomb && Math.random() < 0.10;
                const isSuper = superEnabled && !isGolden && !isBomb && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isGolden && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }
                else if (isGolden) { w = 40; h = 40; }

                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;

                let vy = baseSpeed + Math.random() * 60;
                if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isGolden) vy += 60;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isGolden) type = 'golden';
                else if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';

                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed });
                if (isSuper) sayPlayer('super');"""

if search_str in content:
    content = content.replace(search_str, replace_str)
    with open("index.html", "w") as f:
        f.write(content)
    print("Part 1 Success!")
else:
    print("Part 1 Failed: string not found")
