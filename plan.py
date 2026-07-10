import re

with open('index.html', 'r') as f:
    content = f.read()

print("File len:", len(content))

idx_spawn = content.find("const isFire = isa.enraged")
print("isFire found at:", idx_spawn)

idx_type = content.find("let type = 'normal';")
print("type found at:", idx_type)
