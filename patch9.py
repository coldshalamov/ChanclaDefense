import re

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Make ghost chancla reward score/points
    ghost_reward_search = """                        } else if (c.type === 'trick') {"""
    ghost_reward_replace = """                        } else if (c.type === 'ghost') {
                            gameData.coins += Math.floor(5 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(5 * getPrestigeMultiplier());
                            score += Math.floor(150 * getPrestigeMultiplier());
                            addFloatText('GHOST BUSTED! 👻', c.x, c.y, '#ffffff');
                        } else if (c.type === 'trick') {"""
    content = content.replace(ghost_reward_search, ghost_reward_replace, 1)

    with open(filepath, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
