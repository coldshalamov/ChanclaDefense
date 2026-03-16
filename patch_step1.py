import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add achievements to STATE
    content = content.replace(
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop' };",
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements' };"
    )

    # 2. Add achievements to gameData initialization
    content = content.replace(
        "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 } };",
        "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }, achievements: {} };"
    )

    # 3. Handle backward compatibility missing achievements
    content = content.replace(
        "if (!gameData.stats) gameData.stats = { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 };",
        "if (!gameData.stats) gameData.stats = { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 };\n                if (!gameData.achievements) gameData.achievements = {};"
    )

    # 4. Define ACH_DATA after gameData block
    ach_data_code = """
            const ACH_DATA = [
                { id: 'novice', name: 'Novice Slapper', desc: 'Slap 100 chanclas', type: 'totalSlaps', target: 100, reward: 50 },
                { id: 'pro', name: 'Pro Slapper', desc: 'Slap 500 chanclas', type: 'totalSlaps', target: 500, reward: 150 },
                { id: 'master', name: 'Master Slapper', desc: 'Slap 2000 chanclas', type: 'totalSlaps', target: 2000, reward: 500 },
                { id: 'perfect1', name: 'Good Eye', desc: 'Get 50 Perfect Slaps', type: 'perfectSlaps', target: 50, reward: 100 },
                { id: 'perfect2', name: 'Flawless', desc: 'Get 250 Perfect Slaps', type: 'perfectSlaps', target: 250, reward: 300 },
                { id: 'games1', name: 'Survivor', desc: 'Play 10 games', type: 'gamesPlayed', target: 10, reward: 50 },
                { id: 'games2', name: 'Masochist', desc: 'Play 50 games', type: 'gamesPlayed', target: 50, reward: 200 },
                { id: 'rich', name: 'Money Maker', desc: 'Earn 1000 total coins', type: 'totalCoinsEarned', target: 1000, reward: 300 }
            ];
"""
    content = content.replace(
        "function saveGameData() {\n                localStorage.setItem('chancla_bomb_save', JSON.stringify(gameData));\n            }",
        "function saveGameData() {\n                localStorage.setItem('chancla_bomb_save', JSON.stringify(gameData));\n            }\n" + ach_data_code
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('index.html')
patch_file('chancla_bomb.html')
