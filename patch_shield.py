import re

for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    # Change maxLevel of shield to 1
    old_shield = "{ id: 'shield', name: 'Start Shield', icon: '🛡️', baseCost: 150, maxLevel: 5, desc: 'Start with shield' }"
    new_shield = "{ id: 'shield', name: 'Start Shield', icon: '🛡️', baseCost: 150, maxLevel: 1, desc: 'Start with shield' }"

    if old_shield in content:
        content = content.replace(old_shield, new_shield)
        print(f"Success patch_shield for {filename}")
    else:
        print(f"Old block not found for shield in {filename}!")

    # Also update click logic
    old_click = "{ id: 'shield', baseCost: 150, maxLevel: 5 }"
    new_click = "{ id: 'shield', baseCost: 150, maxLevel: 1 }"

    if old_click in content:
        content = content.replace(old_click, new_click)
        print(f"Success patch_click_shield for {filename}")
    else:
        print(f"Old block not found for click shield in {filename}!")

    with open(filename, 'w') as f:
        f.write(content)
