with open("index.html", "r") as f:
    content = f.read()

start = content.find("function updateChanclas(dt)")
end = content.find("function drawFloatTexts()")

if start != -1 and end != -1:
    print(content[start:end])
