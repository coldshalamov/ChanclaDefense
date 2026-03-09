with open("index.html", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines[1895:1925]):
    print(f"{1895 + i}: {line}", end='')
