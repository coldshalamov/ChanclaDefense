with open("index.html", "r") as f:
    content = f.read()

search_str = """                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';

                // Prioritize Noto Color Emoji"""

replace_str = """                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';
                else if (type === 'golden') emoji = '✨🥴';

                // Prioritize Noto Color Emoji"""

if search_str in content:
    content = content.replace(search_str, replace_str)
    with open("index.html", "w") as f:
        f.write(content)
    print("Part 4 Success!")
else:
    print("Part 4 Failed: string not found")
