import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_test_setup = "        initTitle();\n        })();\n    </script>"
    new_test_setup = """        initTitle();
            window.setSpecial = function(val) { specialAttackBar = val; };
            window.fireSpecial = function() { fireSpecialAttack(); };
            window.applyPowerup = function(p) { applyPowerup(p); };
        })();
    </script>"""

    if old_test_setup in content:
        content = content.replace(old_test_setup, new_test_setup, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Done")
