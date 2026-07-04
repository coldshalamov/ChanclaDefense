with open('index.html', 'r') as f:
    lines = f.readlines()

print("--- drawWinScreen to loop ---")
for i in range(2630, 2655):
    print(f"{i+1}: {lines[i].rstrip()}")
