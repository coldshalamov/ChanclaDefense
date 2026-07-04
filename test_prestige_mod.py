import re
with open('index.html', 'r') as f:
    c = f.read()
if "STATE.PRESTIGE" in c and "drawPrestige()" in c:
    print("SUCCESS: PRESTIGE state is in index.html")
else:
    print("FAILED index.html")

with open('chancla_bomb.html', 'r') as f:
    c = f.read()
if "STATE.PRESTIGE" in c and "drawPrestige()" in c:
    print("SUCCESS: PRESTIGE state is in chancla_bomb.html")
else:
    print("FAILED chancla_bomb.html")
