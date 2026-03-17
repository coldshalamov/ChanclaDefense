import sys
import re

def clean_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Clean up duplicated if (!gameData.achievements) gameData.achievements = {};
    content = content.replace("                if (!gameData.achievements) gameData.achievements = {};\n                if (!gameData.achievements) gameData.achievements = {};", "                if (!gameData.achievements) gameData.achievements = {};")

    # Clean up duplicated Logros button code in drawTitleScreen
    # Let's find the exact block and replace double occurences with single
    dup_logros_btn = """                // Achievements Button
                ctx.fillStyle = '#9b59b6';
                roundRect(ctx, 110, 520, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Logros / Medals', canvas.width / 2, 550);

                // Achievements Button
                ctx.fillStyle = '#9b59b6';
                roundRect(ctx, 110, 520, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Logros / Medals', canvas.width / 2, 550);"""

    single_logros_btn = """                // Achievements Button
                ctx.fillStyle = '#9b59b6';
                roundRect(ctx, 110, 520, canvas.width - 220, 46, 12);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText('Logros / Medals', canvas.width / 2, 550);"""

    content = content.replace(dup_logros_btn, single_logros_btn)

    # Clean up duplicated drawAchievements function
    # It starts with "            function drawAchievements() {" and ends before "            function drawTitleScreen() {"

    parts = content.split("            function drawTitleScreen() {")
    if len(parts) > 1:
        first_part = parts[0]
        # find the last occurence of drawAchievements and the one before it
        # Because we accidentally ran the patch scripts twice on index.html
        idx1 = first_part.find("            function drawAchievements() {")
        idx2 = first_part.find("            function drawAchievements() {", idx1 + 1)

        if idx1 != -1 and idx2 != -1:
            # It's duplicated. We remove the first one.
            content = first_part[:idx1] + first_part[idx2:] + "            function drawTitleScreen() {" + parts[1]

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

clean_file('index.html')
clean_file('chancla_bomb.html')
