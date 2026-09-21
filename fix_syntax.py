import re

def fix_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Clean up literal backslashes from raw string injection
    content = content.replace(r"\'ghost\'", "'ghost'")
    content = content.replace(r"\'👻\'", "'👻'")
    content = content.replace(r"\'sniper\'", "'sniper'")

    with open(filename, 'w') as f:
        f.write(content)

fix_file('index.html')
fix_file('chancla_bomb.html')
print("Syntax errors fixed.")
