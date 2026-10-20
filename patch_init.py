for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    content = content.replace('{ golden_chance: 0, witch_time: 0, combo_shield: 0 }', '{ golden_chance: 0, witch_time: 0, combo_shield: 0, endless_mastery: 0 }')

    with open(filename, 'w') as f:
        f.write(content)
