import re

with open('index.html', 'r') as f:
    content = f.read()

coins_1 = re.search(r"gameData\.stats\.totalCoinsEarned \+= 5 \* c\.rallyCount;", content)
if coins_1: print("C1: ", coins_1.group(0))

coins_2 = re.search(r"gameData\.stats\.totalCoinsEarned \+= 2;", content)
if coins_2: print("C2: ", coins_2.group(0))

coins_3 = re.search(r"gameData\.stats\.totalCoinsEarned \+= 1;", content)
if coins_3: print("C3: ", coins_3.group(0))

coins_4 = re.search(r"gameData\.stats\.totalCoinsEarned \+= bonus;", content)
if coins_4: print("C4: ", coins_4.group(0))

coins_5 = re.search(r"gameData\.stats\.totalCoinsEarned \+= earned;", content)
if coins_5: print("C5: ", coins_5.group(0))
