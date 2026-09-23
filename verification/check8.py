def get_trySlap(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    start = content.find('function trySlap() {')
    end = content.find('function fireSpecialAttack() {')
    print(f"--- {filepath} ---")
    if start != -1 and end != -1:
        print("Found trySlap")
    else:
        print("NOT FOUND")

    m1 = content.find('getPrestigeMultiplier()')
    m2 = content.find('canvas.height')
    m3 = content.find('score += Math.floor')
    m4 = content.find('gameData.stats.totalCoinsEarned')
    m5 = content.find('} else if (isPerfect) {')

    for i, m in enumerate([m1, m2, m3, m4, m5]):
        if m != -1:
            print(f"Match {i+1} found")
        else:
            print(f"Match {i+1} NOT FOUND")

get_trySlap('chancla_bomb.html')
