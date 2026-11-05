import re

for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    # We need a robust string replacement to remove cactus logic
    content = re.sub(r'const isCactus = !isBomb[^;]+;\n\s*', '', content)

    # Spawn assignments
    content = re.sub(r' && !isCactus', '', content)

    # Types and sizes
    content = re.sub(r'else if \(isCactus\) [^\n]+\n\s*', '', content)

    content = re.sub(r'else if \(type === \'cactus\'\) [^\n]+\n\s*', '', content)

    # Slap logic
    slap_regex = r'if \(c\.type === \'cactus\'\) \{\s*c\.slapped = true;.*?continue;\s*\}'
    content = re.sub(slap_regex, '', content, flags=re.DOTALL)

    # Hit logic
    content = re.sub(r'if \(c\.type === \'cactus\'\) continue;\n\s*', '', content)

    # Avoid logic
    avoid_regex = r'if \(c\.type === \'cactus\' && !c\.slapped\) \{\s*score \+=.*?\s*addFloatText.*?\} else if \(c\.type === \'bomb\'\)'
    content = re.sub(avoid_regex, r"if (c.type === 'bomb')", content, flags=re.DOTALL)

    # Drawing background logic
    content = re.sub(r'const cactusShapes = \[\];\n\s*', '', content)
    content = re.sub(r'cactusShapes\.length = 0;\n\s*', '', content)

    bg_push_regex = r'for \(let i = 0; i < 3; i\+\+\) \{\s*const baseX = 60 \+ i \* 120 \+ Math\.random\(\) \* 40;\s*const baseY = canvas\.height - 30;\s*cactusShapes\.push\(\{ baseX, baseY \}\);\s*\}\n\s*'
    content = re.sub(bg_push_regex, '', content, flags=re.DOTALL)

    bg_draw_regex = r'cactusShapes\.forEach\(c => \{.*?\}\);\n\s*'
    content = re.sub(bg_draw_regex, '', content, flags=re.DOTALL)

    with open(filename, 'w') as f:
        f.write(content)

print("Patched cactus logic with regex")
