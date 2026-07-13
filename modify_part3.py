with open("index.html", "r") as f:
    content = f.read()

search_str = """                            if (c.type === 'bomb') damage = 20;
                            if (c.isPerfect) damage += 7;"""

replace_str = """                            if (c.type === 'bomb') damage = 20;
                            if (c.type === 'golden') damage = 35;
                            if (c.isPerfect) damage += 7;"""

if search_str in content:
    content = content.replace(search_str, replace_str)
    with open("index.html", "w") as f:
        f.write(content)
    print("Part 3 Success!")
else:
    print("Part 3 Failed: string not found")
