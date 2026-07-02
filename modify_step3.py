import re

files = ['index.html', 'chancla_bomb.html']

search_str = """                    else if (pos.y >= 560 && pos.y <= 606 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }"""

replace_str = """                    else if (pos.y >= 560 && pos.y <= 606 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.COSMETICS;
                    }
                    // Check Prestige Button (110, 620, w, 46)
                    else if (gameData.stats.wins >= 10 && pos.y >= 620 && pos.y <= 666 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }"""

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # The string exists in both handleClick and handleTouch
    content = content.replace(search_str, replace_str)

    with open(filename, 'w') as f:
        f.write(content)

print("Step 3 done")
