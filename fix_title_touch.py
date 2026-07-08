import re

with open('index.html', 'r') as f:
    content = f.read()

# Make directions visible toggle hide when going to PRESTIGE state
# In drawTitleScreen click
old_click = """                    // Check Prestige Button
                    else if (gameData.stats.wins >= 10 && pos.y >= 620 && pos.y <= 666 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }"""
content = content.replace(old_click, old_click)

# In touchstart
old_touch = """                    else if (gameData.stats.wins >= 10 && pos.y >= 620 && pos.y <= 666 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        setDirectionsVisible(false);
                        state = STATE.PRESTIGE;
                    }"""
content = content.replace(old_touch, old_touch)

with open('index.html', 'w') as f:
    f.write(content)
