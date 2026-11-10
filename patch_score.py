import sys

def patch_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    search1 = """                        comboCount++;
                        comboTimer = 2.5;
                        if (comboCount > (gameData.stats.maxCombo || 0)) gameData.stats.maxCombo = comboCount;
                        score += Math.floor(comboCount * getPrestigeMultiplier());"""
    replace1 = """                        comboCount++;
                        comboTimer = 2.5;
                        if (comboCount > (gameData.stats.maxCombo || 0)) gameData.stats.maxCombo = comboCount;

                        let comboMult = 1.0;
                        if (comboCount >= 25) comboMult = 2.0;
                        else if (comboCount >= 10) comboMult = 1.5;

                        score += Math.floor(comboCount * getPrestigeMultiplier() * comboMult);"""

    search2 = """                            // Hit Isa
                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);
                            if (c.type === 'meteor') damage = 40;
                            if (c.type === 'bomb') damage = 20;
                            if (c.type === 'blackhole') damage = 25;
                            if (c.type === 'golden') damage = 0; // Prevent double-dipping as damage is applied in trySlap



                            if (c.isPerfect) damage += 7;
                            damage += (gameData.upgrades.power || 0) * 2;"""
    replace2 = """                            // Hit Isa
                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);
                            if (c.type === 'meteor') damage = 40;
                            if (c.type === 'bomb') damage = 20;
                            if (c.type === 'blackhole') damage = 25;
                            if (c.type === 'golden') damage = 0; // Prevent double-dipping as damage is applied in trySlap

                            let dmgMult = 1.0 + Math.min(1.0, Math.floor(comboCount / 5) * 0.1);
                            damage = damage * dmgMult;

                            if (c.isPerfect) damage += 7;
                            damage += (gameData.upgrades.power || 0) * 2;"""

    if search1 in content and search2 in content:
        content = content.replace(search1, replace1)
        content = content.replace(search2, replace2)
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Successfully patched {filename}")
    else:
        print(f"Failed to find search blocks in {filename}")

patch_file('index.html')
patch_file('chancla_bomb.html')
