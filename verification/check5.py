import re

def get_blocks(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    b1 = re.search(r"\} else if \(isPerfect\) \{", content)
    if b1:
        print("--- Block 1 ---")
        print(b1.group(0))

    b2 = re.search(r"gameData\.coins \+= Math\.floor", content)
    if b2:
        print("--- Block 2 ---")
        print(b2.group(0))

get_blocks('index.html')
