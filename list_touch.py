with open('index.html', 'r') as f:
    lines = f.readlines()

for i in range(2810, 2835):
    print(f"{i+1}: {lines[i].rstrip()}")
