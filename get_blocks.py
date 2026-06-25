with open('index.html', 'r') as f:
    content = f.read()

import re

# 1. spawnChancla
m1 = re.search(r'(const isFire = .*?\n.*?let w = 32;\n.*?let h = 18;)', content, re.MULTILINE)
print("--- BLOCK 1 ---")
if m1: print(m1.group(0))

# 2. spawnChancla type
m2 = re.search(r'(let type = \'normal\';\n.*?if \(isBomb\) type = \'bomb\';\n.*?else if \(isFire\) type = \'fire\';\n.*?else if \(isSuper\) type = \'super\';\n.*?else if \(isHoming\) type = \'homing\';)', content, re.MULTILINE)
print("--- BLOCK 2 ---")
if m2: print(m2.group(0))

# 3. drawChancla emoji
m3 = re.search(r'(let emoji = \'🩴💨\';\n.*?if \(type === \'super\'\) emoji = \'🩴💥\';\n.*?else if \(type === \'fire\'\) emoji = \'🔥\';\n.*?else if \(type === \'bomb\'\) emoji = \'💣\';\n.*?else if \(type === \'homing\'\) emoji = \'🪬\';)', content, re.MULTILINE)
print("--- BLOCK 3 ---")
if m3: print(m3.group(0))

# 4. drawChancla shadow
m4 = re.search(r'(} else if \(type === \'homing\'\) {\n.*?ctx\.shadowColor = \'#8a2be2\';\n.*?ctx\.shadowBlur = 15;\n.*?})', content, re.MULTILINE)
print("--- BLOCK 4 ---")
if m4: print(m4.group(0))

# 6. updateChanclas homing logic
m6 = re.search(r'(// Homing Logic\n.*?if \(c\.type === \'homing\' && !c\.slapped\) \{\n.*?const targetX = player\.x;\n.*?const directionX = Math\.sign\(targetX - c\.x\);\n.*?// Smoothly accelerate towards the player\'s X coordinate\n.*?c\.vx \+= directionX \* 200 \* dt; // Acceleration factor\n.*?// Cap maximum horizontal speed to ensure it\'s still dodgeable\n.*?const maxHomingSpeed = 150;\n.*?if \(Math\.abs\(c\.vx\) > maxHomingSpeed\) \{\n.*?c\.vx = Math\.sign\(c\.vx\) \* maxHomingSpeed;\n.*?\}\n.*?\})', content, re.DOTALL)
print("--- BLOCK 6 ---")
if m6: print(m6.group(0))

# 7. updateChanclas collision overlap
m7 = re.search(r'(if \(!c\.slapped && c\.type !== \'meteor\' && rectsOverlap\(player, c\)\) \{)', content, re.MULTILINE)
print("--- BLOCK 7 ---")
if m7: print(m7.group(0))

# 8. spawnChancla vy
m8 = re.search(r'(let vy = baseSpeed \+ Math\.random\(\) \* 60;\n.*?if \(isSuper\) vy \+= 40;\n.*?else if \(isFire\) vy \+= 80;\n.*?else if \(isBomb\) vy = baseSpeed \* 0\.7 \+ Math\.random\(\) \* 30; // slower\n.*?else if \(isHoming\) vy = baseSpeed \* 0\.8; // slightly slower vertical speed)', content, re.MULTILINE)
print("--- BLOCK 8 ---")
if m8: print(m8.group(0))

# 9. addFloatText
m9 = re.search(r'(function addFloatText\(text, x, y.*?\) \{\n.*?floatTexts\.push\(\{ text, x, y, time: 1\.8, max: 1\.8 .*?\}\);\n.*?\})', content, re.MULTILINE)
print("--- BLOCK 9 ---")
if m9: print(m9.group(0))

# 10. trySlap loop golden slap
m10 = re.search(r'(if \(isPerfect\) gameData\.stats\.perfectSlaps\+\+;)', content, re.MULTILINE)
print("--- BLOCK 10 ---")
if m10: print(m10.group(0))
