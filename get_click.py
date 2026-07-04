with open('index.html', 'r') as f:
    lines = f.readlines()
for i in range(2705, 2720):
    print(f"{i+1}: {lines[i].rstrip()}")
