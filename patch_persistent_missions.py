import sys

def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # 1. Add persistent_missions to initialization objects
    content = content.replace(
        "if (!gameData.prestigeUpgrades) gameData.prestigeUpgrades = { golden_chance: 0, witch_time: 0, combo_shield: 0, endless_mastery: 0 };",
        "if (!gameData.prestigeUpgrades) gameData.prestigeUpgrades = { golden_chance: 0, witch_time: 0, combo_shield: 0, endless_mastery: 0, persistent_missions: 0 };"
    )

    # 2. Update logic for keeping unfinished missions
    mission_replace = """                if (!gameData.missions || gameData.missions.date !== today) {"""

    mission_new = """                // If they have the upgrade, do not clear unfinished missions
                let keepMissions = false;
                if (gameData.prestigeUpgrades && gameData.prestigeUpgrades.persistent_missions) {
                    if (gameData.missions && gameData.missions.list) {
                        const anyUnfinished = gameData.missions.list.some(m => !m.claimed);
                        if (anyUnfinished) {
                            keepMissions = true;
                        }
                    }
                }

                if (!keepMissions && (!gameData.missions || gameData.missions.date !== today)) {"""
    content = content.replace(mission_replace, mission_new)

    # 3. Add to prestigeUpgradesList display
    list_replace = """                    { id: 'endless_mastery', name: 'Endless Mastery', icon: '♾️', cost: 3, maxLevel: 3, desc: 'Endless Best boosts Mult' }
                ];"""

    list_new = """                    { id: 'endless_mastery', name: 'Endless Mastery', icon: '♾️', cost: 3, maxLevel: 3, desc: 'Endless Best boosts Mult' },
                    { id: 'persistent_missions', name: 'Mission Master', icon: '📜', cost: 2, maxLevel: 1, desc: 'Keep unfinished missions' }
                ];"""
    content = content.replace(list_replace, list_new)

    # 4. Add to click handlers
    click_replace = """                        { id: 'endless_mastery', cost: 3, maxLevel: 3 }
                    ];"""
    click_new = """                        { id: 'endless_mastery', cost: 3, maxLevel: 3 },
                        { id: 'persistent_missions', cost: 2, maxLevel: 1 }
                    ];"""
    content = content.replace(click_replace, click_new)

    with open(filepath, "w") as f:
        f.write(content)

if __name__ == '__main__':
    patch_file("index.html")
    patch_file("chancla_bomb.html")
