import sys

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Revert the specific wrong replacement
    content = content.replace("let shakeTimer = 0;\n                slowMoTimer = 0;", "let shakeTimer = 0;")

    with open(filepath, 'w') as f:
        f.write(content)

fix_file('index.html')
fix_file('chancla_bomb.html')
