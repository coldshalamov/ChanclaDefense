import sys

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    target_snippet = """                isa.anger = isa.maxAnger;
                isa.x = canvas.width / 2;"""

    replacement = """                isa.anger = isa.maxAnger;
                isa.displayAnger = isa.maxAnger;
                isa.x = canvas.width / 2;"""

    if target_snippet not in content:
        print(f"Target snippet not found in {filepath} (Step 2)")
        return

    content = content.replace(target_snippet, replacement)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath}")

replace_in_file('index.html')
replace_in_file('chancla_bomb.html')
