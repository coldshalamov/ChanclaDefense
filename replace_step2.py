import os

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replacements
    target1 = "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics' };"
    replacement1 = "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics', PRESTIGE: 'prestige' };"

    if target1 in content:
        content = content.replace(target1, replacement1)
    else:
        print(f"Failed to find target1 in {filepath}")

    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file("index.html")
replace_in_file("chancla_bomb.html")
