import sys

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    replacements = [
        (
            "                roundRect(ctx, 30, 260, canvas.width - 60, 200, 16);",
            "                // Expand box if level >= 10 to fit Prestige button\n                if (gameData.stats.wins >= 10) {\n                    roundRect(ctx, 30, 260, canvas.width - 60, 420, 16);\n                } else {\n                    roundRect(ctx, 30, 260, canvas.width - 60, 360, 16);\n                }"
        )
    ]

    # Try replacements
    for i, (search, replace) in enumerate(replacements):
        if search not in content:
            print(f"Warning: Match {i} not found in {filepath}!")
        else:
            content = content.replace(search, replace, 1)

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Successfully processed {filepath}")

replace_in_file('index.html')
replace_in_file('chancla_bomb.html')
