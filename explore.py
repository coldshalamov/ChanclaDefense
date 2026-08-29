import re

with open('index.html', 'r') as f:
    content = f.read()

# Look for chancla types
types = re.findall(r"type === '(\w+)'", content)
print("Chancla types found:", set(types))

# Look for trySlap
match = re.search(r'function trySlap.*?\{.*?(function|})', content, re.DOTALL)
if match:
    print("trySlap snippet:")
    print(content[match.start():match.start()+1000])
