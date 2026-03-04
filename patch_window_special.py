import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Add window testing exports at the end of the IIFE
    old_end = "initTitle();\n        })();\n    </script>\n</body>\n\n</html>"
    new_end = "initTitle();\n\n            window.setSpecial = (val) => { specialAttackBar = val; };\n            window.fireSpecial = () => { fireSpecialAttack(); };\n        })();\n    </script>\n</body>\n\n</html>"

    if "window.setSpecial =" not in content:
        content = content.replace(old_end, new_end, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Patched window special exports.")
