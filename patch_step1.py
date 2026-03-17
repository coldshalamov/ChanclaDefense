import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Patch 1: Add STATE.ACHIEVEMENTS
    old_state = "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop' };"
    new_state = "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements' };"
    if old_state in content:
        content = content.replace(old_state, new_state, 1)

    # Patch 2: Initialize achievements in gameData
    old_gameData = "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 } };"
    new_gameData = "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }, achievements: {} };"
    if old_gameData in content:
        content = content.replace(old_gameData, new_gameData, 1)

    # Patch 3: Backward compatibility for achievements
    old_stats_init = "if (!gameData.stats) gameData.stats = { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 };"
    new_stats_init = "if (!gameData.stats) gameData.stats = { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 };\n                if (!gameData.achievements) gameData.achievements = {};"
    if old_stats_init in content:
        content = content.replace(old_stats_init, new_stats_init, 1)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('chancla_bomb.html')
