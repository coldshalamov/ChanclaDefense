with open("index.html", "r") as f:
    content = f.read()

start = content.find("function trySlap()")
end = content.find("function fireSpecialAttack()")

if start != -1 and end != -1:
    print(content[start:end])
