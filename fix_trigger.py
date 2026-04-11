import re

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    correct_func = """
            function triggerWin() {
                state = STATE.WIN;

                // Base 50 + (wins * 50) as bonus based on current boss level
                let bonus = 50 + (gameData.stats.wins * 50);
                gameData.coins += bonus;
                gameData.stats.totalCoinsEarned += bonus;

                gameData.stats.wins++;

                saveGameData();
                sayRandom('win');
            }
"""

    content = re.sub(r'            function triggerWin\(\) \{.*?\n            \}', correct_func.strip('\n'), content, flags=re.DOTALL)

    with open(filename, 'w') as f:
        f.write(content)

update_file('index.html')
update_file('chancla_bomb.html')
