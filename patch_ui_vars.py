for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    # prestigeUpgradesList UI
    old_list_ui = """                const prestigeUpgradesList = [
                    { id: 'golden_chance', name: 'Golden Touch', icon: '✨', cost: 1, maxLevel: 3, desc: '+2% Golden Chancla chance' },
                    { id: 'witch_time', name: 'Time Wizard', icon: '⏳', cost: 1, maxLevel: 3, desc: '+0.5s Witch Time' },
                    { id: 'combo_shield', name: 'Combo Shield', icon: '🛡️', cost: 2, maxLevel: 1, desc: 'Shield at 30 combo' }
                ];"""
    new_list_ui = """                const prestigeUpgradesList = [
                    { id: 'golden_chance', name: 'Golden Touch', icon: '✨', cost: 1, maxLevel: 3, desc: '+2% Golden Chancla chance' },
                    { id: 'witch_time', name: 'Time Wizard', icon: '⏳', cost: 1, maxLevel: 3, desc: '+0.5s Witch Time' },
                    { id: 'combo_shield', name: 'Combo Shield', icon: '🛡️', cost: 2, maxLevel: 1, desc: 'Shield at 30 combo' },
                    { id: 'endless_mastery', name: 'Endless Mastery', icon: '♾️', cost: 3, maxLevel: 3, desc: 'Endless Best boosts Mult' }
                ];"""
    content = content.replace(old_list_ui, new_list_ui)

    # prestige handlers list
    old_handler_list = """                    const prestigeUpgradesList = [
                        { id: 'golden_chance', cost: 1, maxLevel: 3 },
                        { id: 'witch_time', cost: 1, maxLevel: 3 },
                        { id: 'combo_shield', cost: 2, maxLevel: 1 }
                    ];"""
    new_handler_list = """                    const prestigeUpgradesList = [
                        { id: 'golden_chance', cost: 1, maxLevel: 3 },
                        { id: 'witch_time', cost: 1, maxLevel: 3 },
                        { id: 'combo_shield', cost: 2, maxLevel: 1 },
                        { id: 'endless_mastery', cost: 3, maxLevel: 3 }
                    ];"""
    content = content.replace(old_handler_list, new_handler_list)

    with open(filename, 'w') as f:
        f.write(content)
