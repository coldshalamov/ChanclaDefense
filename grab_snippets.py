import re

files = ['index.html']
for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # STATE
    print("--- STATE ---")
    state_match = re.search(r"const STATE = \{[^}]*\};", content)
    if state_match:
        print(state_match.group(0))

    # GAMEDATA init
    print("\n--- GAMEDATA INIT ---")
    gd_match = re.search(r"let gameData = \{.*?\};", content)
    if gd_match:
        print(gd_match.group(0))

    # PRESTIGE INIT (localStorage)
    print("\n--- PRESTIGE INIT ---")
    ginit_match = re.search(r"if \(!gameData\.currentHat\) gameData\.currentHat = 'none';", content)
    if ginit_match:
        print(ginit_match.group(0))

    # LOOP
    print("\n--- LOOP DRAW ---")
    loop_match = re.search(r"else if \(state === STATE\.COSMETICS\) drawCosmetics\(\);", content)
    if loop_match:
        print(loop_match.group(0))

    # TITLE BUTTON
    print("\n--- TITLE BUTTON DRAW ---")
    title_btn_match = re.search(r"ctx\.fillText\('Cosmetics / Cosm\.', canvas\.width / 2, 590\);\n\n                ctx\.restore\(\);", content)
    if title_btn_match:
        print(title_btn_match.group(0))

    # TITLE CLICK
    print("\n--- TITLE CLICK ---")
    click_match = re.search(r"else if \(pos\.y >= 560 && pos\.y <= 606 && pos\.x >= 110 && pos\.x <= canvas\.width - 110\) \{\n\s*setDirectionsVisible\(false\);\n\s*state = STATE\.COSMETICS;\n\s*\}", content)
    if click_match:
        print(click_match.group(0))
