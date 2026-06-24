import re

with open('index.html', 'r') as f:
    content = f.read()

types_match = re.search(r'const isFire = (.*?);', content)
print(types_match)

# Let's just find "type:" assignments
import re
types = set(re.findall(r'type:\s*[\'"]([a-zA-Z]+)[\'"]', content))
print("Types found:", types)
