import re

for filename in ['index.html']:
    with open(filename, 'r') as f:
        content = f.read()

    print("\n--- GLOBAL HELPER ---")
    helper_match = re.search(r"let hitStop = 0;", content)
    if helper_match:
        print(helper_match.group(0))

    print("\n--- COIN ACQ 1 ---")
    coin_match = re.search(r"score \+= 20 \* c\.rallyCount;\n\s*gameData\.coins \+= 5 \* c\.rallyCount;", content)
    if coin_match:
        print(coin_match.group(0))

    print("\n--- COIN ACQ 2 ---")
    coin2_match = re.search(r"if \(isPerfect\) \{\n\s*gameData\.coins \+= 2;", content)
    if coin2_match:
        print(coin2_match.group(0))

    print("\n--- COIN ACQ 3 ---")
    coin3_match = re.search(r"\} else \{\n\s*gameData\.coins \+= 1;", content)
    if coin3_match:
        print(coin3_match.group(0))

    print("\n--- SCORE PASSIVE ---")
    score1_match = re.search(r"score \+= dt \* 50; // passive score", content)
    if score1_match:
        print(score1_match.group(0))
