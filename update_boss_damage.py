import re
with open('index.html', 'r') as f:
    content = f.read()

match = re.search(r'let damage = .*?isa\.anger -= damage', content, re.DOTALL)
if match:
    print("Found boss damage snippet:")
    print(content[match.start()-200:match.start()+500])
else:
    # Try another search
    match = re.search(r'isa\.anger -=', content)
    if match:
        print(content[match.start()-200:match.start()+500])
