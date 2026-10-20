for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    old_mult = """            function getPrestigeMultiplier() {
                let mult = (1 + (gameData.prestige || 0) * 0.5) * (1 + (gameData.upgrades.greed || 0) * 0.1);
                if (gameData.hardMode) mult *= 2;
                return mult;
            }"""
    new_mult = """            function getPrestigeMultiplier() {
                let mult = (1 + (gameData.prestige || 0) * 0.5) * (1 + (gameData.upgrades.greed || 0) * 0.1);
                if (gameData.prestigeUpgrades && gameData.prestigeUpgrades.endless_mastery) {
                    mult += (gameData.prestigeUpgrades.endless_mastery * (gameData.endlessBestScore || 0) * 0.0001);
                }
                if (gameData.hardMode) mult *= 2;
                return mult;
            }"""
    content = content.replace(old_mult, new_mult)

    with open(filename, 'w') as f:
        f.write(content)
