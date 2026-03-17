import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We need to hide the directions when entering ACHIEVEMENTS state
    # Patch 1: Click logic
    old_ach_clicks_enter = """                    // Check Achievements Button (110, 520, w, 46)
                    else if (pos.y >= 520 && pos.y <= 566 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.ACHIEVEMENTS;
                    }"""
    new_ach_clicks_enter = """                    // Check Achievements Button (110, 520, w, 46)
                    else if (pos.y >= 520 && pos.y <= 566 && pos.x >= 110 && pos.x <= canvas.width - 110) {
                        state = STATE.ACHIEVEMENTS;
                        setDirectionsVisible(false);
                    }"""

    old_ach_clicks_back = """                    // Check Back Button
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 34 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                    }"""
    new_ach_clicks_back = """                    // Check Back Button
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 34 && pos.x >= 100 && pos.x <= canvas.width - 100) {
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }"""

    # Patch 2: Touch logic
    old_ach_touch_enter = """                    else if (pos.y >= 520 && pos.y <= 566) state = STATE.ACHIEVEMENTS;
                    return;
                }"""
    new_ach_touch_enter = """                    else if (pos.y >= 520 && pos.y <= 566) {
                        state = STATE.ACHIEVEMENTS;
                        setDirectionsVisible(false);
                    }
                    return;
                }"""

    old_ach_touch_back = """                    // Check Back Button
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 34) {
                        state = STATE.TITLE;
                    }"""
    new_ach_touch_back = """                    // Check Back Button
                    if (pos.y >= canvas.height - 80 && pos.y <= canvas.height - 34) {
                        state = STATE.TITLE;
                        setDirectionsVisible(true);
                    }"""

    if old_ach_clicks_enter in content:
        content = content.replace(old_ach_clicks_enter, new_ach_clicks_enter, 1)
    if old_ach_clicks_back in content:
        content = content.replace(old_ach_clicks_back, new_ach_clicks_back, 1)
    if old_ach_touch_enter in content:
        content = content.replace(old_ach_touch_enter, new_ach_touch_enter, 1)
    if old_ach_touch_back in content:
        content = content.replace(old_ach_touch_back, new_ach_touch_back, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('index.html')
patch_file('chancla_bomb.html')
