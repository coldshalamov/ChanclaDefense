import re

with open('index.html', 'r') as f:
    content = f.read()

match = re.search(r'function spawnChancla.*?\{.*?(function|})', content, re.DOTALL)
if match:
    print("spawnChancla snippet:")
    print(content[match.start():match.start()+1500])
