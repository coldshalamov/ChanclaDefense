import re
with open('index.html', 'r') as f:
    content = f.read()

match = re.search(r'function trySlap\(\).*?updateMissionProgress\(\'slap\', 1\);.*?isPerfect.*?let basePts', content, re.DOTALL)
if match:
    print("Found match!")
    # print(content[match.start():match.start()+2500])
else:
    print("Not found")
