with open('index.html', 'r') as f:
    lines = f.readlines()

print("--- drawTitleScreen End ---")
for i in range(1700, 1720):
    print(f"{i+1}: {lines[i].rstrip()}")

print("\n--- Click Listener End of TITLE ---")
for i in range(2705, 2715):
    print(f"{i+1}: {lines[i].rstrip()}")

print("\n--- Touch Listener End of TITLE ---")
for i in range(2820, 2835):
    print(f"{i+1}: {lines[i].rstrip()}")
