with open("index.html", "r") as f:
    lines = f.readlines()

def print_around(pattern, context=10):
    for i, line in enumerate(lines):
        if pattern in line:
            start = max(0, i - context)
            end = min(len(lines), i + context + 1)
            print(f"--- MATCH: {pattern} ---")
            for j in range(start, end):
                print(repr(lines[j]))
            print("\n")
            return

print_around("const rotSpeed = (Math.random()")
