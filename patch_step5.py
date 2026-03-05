import re

with open('index.html', 'r') as f:
    content = f.read()

# Expose testing functions to window
test_funcs_old = """            function initTitle() {
                sayRandom('start');
                setDirectionsVisible(true);
            }
            initTitle();
        })();
    </script>"""
test_funcs_new = """            function initTitle() {
                sayRandom('start');
                setDirectionsVisible(true);
            }
            initTitle();

            // Expose for testing
            window.setSpecial = (val) => { specialAttackBar = val; };
            window.fireSpecial = () => { trySlap(); };
        })();
    </script>"""
content = content.replace(test_funcs_old, test_funcs_new, 1)

with open('index.html', 'w') as f:
    f.write(content)
