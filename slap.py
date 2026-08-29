import re
with open('index.html', 'r') as f:
    content = f.read()

match = re.search(r'function trySlap\(.*?\).*?isa.anger -= damage;', content, re.DOTALL)
if match:
    print(content[match.start():match.start()+2000])
