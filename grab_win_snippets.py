import re

for filename in ['index.html']:
    with open(filename, 'r') as f:
        content = f.read()

    print("\n--- COIN ACQ BOSS BONUS ---")
    boss_bonus_match = re.search(r"const bonus = 50 \+ \(defeatedLevel - 1\) \* 50;\n\s*gameData\.coins \+= bonus;", content)
    if boss_bonus_match:
        print(boss_bonus_match.group(0))

    print("\n--- COIN ACQ END GAME BONUS ---")
    end_game_bonus_match = re.search(r"const earned = Math\.floor\(score / 10\);\n\s*gameData\.coins \+= earned;", content)
    if end_game_bonus_match:
        print(end_game_bonus_match.group(0))

    print("\n--- DRAW PRESTIGE FUNCTION POS ---")
    draw_match = re.search(r"function drawCosmetics\(\) \{", content)
    if draw_match:
        print(draw_match.group(0))

    print("\n--- RESET PRESTIGE STATS ---")
    reset_match = re.search(r"if \(!gameData\.stats\) gameData\.stats = \{ totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 \};", content)
    if reset_match:
        print(reset_match.group(0))
