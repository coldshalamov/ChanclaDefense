import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    search_str = """            function initTitle() {
                sayRandom('start');
                setDirectionsVisible(true);
            }
            initTitle();
        })();"""

    replace_str = """            function initTitle() {
                sayRandom('start');
                setDirectionsVisible(true);
            }
            initTitle();

            // Expose for testing
            window.setSpecial = (val) => specialAttackBar = val;
            window.fireSpecial = fireSpecialAttack;
        })();"""

    if search_str not in content:
        print(f"Could not find search string in {filepath}")
        return

    content = content.replace(search_str, replace_str, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath} window functions")

patch_file('index.html')
patch_file('chancla_bomb.html')
