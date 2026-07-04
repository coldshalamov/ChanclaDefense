with open('index.html', 'r') as f:
    lines = f.readlines()

for i in range(1660, 1720):
    print(f"{i+1}: {lines[i].rstrip()}")
