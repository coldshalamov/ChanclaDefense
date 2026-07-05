import re

for filename in ['index.html']:
    with open(filename, 'r') as f:
        content = f.read()

    print("\n--- SCORE 1 ---")
    score_1 = re.search(r"score \+= comboCount;", content)
    if score_1: print(score_1.group(0))

    print("\n--- SCORE 2 ---")
    score_2 = re.search(r"score \+= 5 \+ comboCount;", content)
    if score_2: print(score_2.group(0))

    print("\n--- SCORE 3 ---")
    score_3 = re.search(r"score \+= 1;", content)
    if score_3: print(score_3.group(0))
