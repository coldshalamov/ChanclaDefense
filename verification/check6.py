import re

def get_blocks(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # get variables usage
    m1 = re.search(r"getPrestigeMultiplier\(\)", content)
    if m1:
        print("getPrestigeMultiplier found")

    m2 = re.search(r"canvas\.height", content)
    if m2:
        print("canvas.height found")

    m3 = re.search(r"score \+= Math\.floor", content)
    if m3:
        print("score += Math.floor found")
        print(m3.group(0))

    m4 = re.search(r"gameData\.stats\.totalCoinsEarned", content)
    if m4:
        print("gameData.stats.totalCoinsEarned found")

get_blocks('index.html')
