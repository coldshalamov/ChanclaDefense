with open('index.html', 'r') as f:
    content = f.read()

import re

# Block 1
m1 = re.search(r'(const isSuper = superEnabled && !isBomb && !isHoming && Math\.random\(\) < 0\.18;\n\s+const isFire = isa\.enraged && !isBomb && !isHoming && !isSuper && Math\.random\(\) < 0\.25;\n\n\s+let w = 32;\n\s+let h = 18;\n\s+if \(isSuper\) \{ w = 46; h = 26; \}\n\s+else if \(isBomb\) \{ w = 38; h = 38; \}\n\s+else if \(isHoming\) \{ w = 36; h = 36; \})', content)
print("Block 1:", bool(m1))

# Block 2
m2 = re.search(r'(let vy = baseSpeed \+ Math\.random\(\) \* 60;\n\s+if \(isSuper\) vy \+= 40;\n\s+else if \(isFire\) vy \+= 80;\n\s+else if \(isBomb\) vy = baseSpeed \* 0\.7 \+ Math\.random\(\) \* 30; // slower\n\s+else if \(isHoming\) vy = baseSpeed \* 0\.8; // slightly slower vertical speed)', content)
print("Block 2:", bool(m2))

# Block 3
m3 = re.search(r'(const vx = \(Math\.random\(\) - 0\.5\) \* 60;\n\s+const rotSpeed = \(Math\.random\(\) - 0\.5\) \* 5;)', content)
print("Block 3:", bool(m3))

# Block 4
m4 = re.search(r'(let type = \'normal\';\n\s+if \(isBomb\) type = \'bomb\';\n\s+else if \(isFire\) type = \'fire\';\n\s+else if \(isSuper\) type = \'super\';\n\s+else if \(isHoming\) type = \'homing\';\n\n\s+chanclas\.push\(\{ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed \}\);)', content)
print("Block 4:", bool(m4))

# Block 5
m5 = re.search(r'(let emoji = \'🩴💨\';\n\s+if \(type === \'super\'\) emoji = \'🩴💥\';\n\s+else if \(type === \'fire\'\) emoji = \'🔥\';\n\s+else if \(type === \'bomb\'\) emoji = \'💣\';\n\s+else if \(type === \'homing\'\) emoji = \'🪬\';)', content)
print("Block 5:", bool(m5))

# Block 6
m6 = re.search(r'(\} else if \(type === \'homing\'\) \{\n\s+ctx\.shadowColor = \'#8a2be2\';\n\s+ctx\.shadowBlur = 15;\n\s+\})', content)
print("Block 6:", bool(m6))

# Block 7
m7 = re.search(r'(// Homing Logic\n\s+if \(c\.type === \'homing\' && !c\.slapped\) \{\n\s+const targetX = player\.x;\n\s+const directionX = Math\.sign\(targetX - c\.x\);\n\s+// Smoothly accelerate towards the player\'s X coordinate\n\s+c\.vx \+= directionX \* 200 \* dt; // Acceleration factor\n\s+// Cap maximum horizontal speed to ensure it\'s still dodgeable\n\s+const maxHomingSpeed = 150;\n\s+if \(Math\.abs\(c\.vx\) > maxHomingSpeed\) \{\n\s+c\.vx = Math\.sign\(c\.vx\) \* maxHomingSpeed;\n\s+\}\n\s+\}\n\n\s+c\.x \+= c\.vx \* dt;)', content)
print("Block 7:", bool(m7))

# Block 8
m8 = re.search(r'(if \(!c\.slapped && c\.type !== \'meteor\' && rectsOverlap\(player, c\)\) \{)', content)
print("Block 8:", bool(m8))

# Block 9
m9 = re.search(r'(if \(dist < slapRange\) \{\n\s+// Slap the chancla away\n\s+const isPerfect = dist < perfectRange;\n\n\s+gameData\.stats\.totalSlaps\+\+;\n\s+if \(isPerfect\) gameData\.stats\.perfectSlaps\+\+;)', content)
print("Block 9:", bool(m9))
