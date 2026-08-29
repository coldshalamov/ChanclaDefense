import re

with open('index.html', 'r') as f:
    content = f.read()

# Check drawChanclas to add Trick rendering
match = re.search(r'function drawChanclas.*?\{.*?(function|})', content, re.DOTALL)
if match:
    print("drawChanclas snippet:")
    print(content[match.start():match.start()+1500])
