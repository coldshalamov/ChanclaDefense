import os

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    search = """                const isBomb = Math.random() < 0.08;
                const isGolden = !isBomb && Math.random() < 0.05;
                const isBoomerang = !isBomb && !isGolden && Math.random() < 0.15;
                const isHoming = superEnabled && !isBomb && !isGolden && !isBoomerang && Math.random() < 0.10;
                const isSuper = superEnabled && !isBomb && !isHoming && !isGolden && !isBoomerang && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }
                else if (isGolden) { w = 36; h = 20; }
                else if (isBoomerang) { w = 34; h = 16; }

                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;

                let vy = baseSpeed + Math.random() * 60;
                if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed
                else if (isGolden) vy += 20; // slightly faster
                else if (isBoomerang) vy += 10;"""

    # Need to check original file as well, oh right I already applied changes above. Let's make sure it matches.
    print(search in content)
modify_file('index.html')
