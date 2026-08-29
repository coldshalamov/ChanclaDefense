import re
with open('index.html', 'r') as f:
    content = f.read()

match = re.search(r'function trySlap\(.*?\{.*?(function|})', content, re.DOTALL)
if match:
    print(content[match.start():match.start()+2500])
