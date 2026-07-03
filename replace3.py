import sys

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    target_snippet = """                if (isa.anger <= isa.maxAnger * 0.3 && !isa.enraged) {
                    isa.enraged = true;"""

    replacement = """                if (isa.displayAnger === undefined) isa.displayAnger = isa.anger;
                if (isa.displayAnger > isa.anger) {
                    isa.displayAnger -= Math.max(30, (isa.displayAnger - isa.anger) * 5) * dt;
                    if (isa.displayAnger < isa.anger) isa.displayAnger = isa.anger;
                } else {
                    isa.displayAnger = isa.anger;
                }

                if (isa.anger <= isa.maxAnger * 0.3 && !isa.enraged) {
                    isa.enraged = true;"""

    if target_snippet not in content:
        print(f"Target snippet not found in {filepath} (Step 3)")
        return

    content = content.replace(target_snippet, replacement)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath}")

replace_in_file('index.html')
replace_in_file('chancla_bomb.html')
