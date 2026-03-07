import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_collision = "if (!c.slapped && rectsOverlap(player, c)) {"
    new_collision = "if (!c.slapped && rectsOverlap(player, c) && (player.hitTimer || 0) <= 0 && (player.dashTimer || 0) <= 0) {"

    if old_collision in content:
        content = content.replace(old_collision, new_collision, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Done")
