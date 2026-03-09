import re

files = ['index.html', 'chancla_bomb.html']

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Add window.fireSpecial back in just for tests at the end
    end_script = "        })();\n    </script>\n</body>"
    new_end_script = "            window.setSpecial = (val) => { specialAttackBar = val; };\n            window.fireSpecial = fireSpecialAttack;\n        })();\n    </script>\n</body>"

    content = content.replace(end_script, new_end_script)

    with open(filepath, 'w') as f:
        f.write(content)

print("Patch applied.")
