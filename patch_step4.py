import sys

def patch_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Patch invincibility in updateChanclas
    old_overlap = "if (!c.slapped && rectsOverlap(player, c)) {"
    new_overlap = "if (!c.slapped && rectsOverlap(player, c) && player.dashTimer <= 0) {"

    if old_overlap in content:
        content = content.replace(old_overlap, new_overlap)
        print(f"Patched invincibility in {filename}")
    else:
        print(f"Could not find old_overlap in {filename}")

    with open(filename, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
