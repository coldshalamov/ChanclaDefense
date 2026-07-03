import sys

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    target_snippet = "const isa = { x: canvas.width / 2, y: 70, anger: 100, maxAnger: 100, hitTimer: 0, enraged: false };"
    replacement = "const isa = { x: canvas.width / 2, y: 70, anger: 100, displayAnger: 100, maxAnger: 100, hitTimer: 0, enraged: false };"

    if target_snippet not in content:
        print(f"Target snippet not found in {filepath} (Step 1)")
        return

    content = content.replace(target_snippet, replacement)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath}")

replace_in_file('index.html')
replace_in_file('chancla_bomb.html')
