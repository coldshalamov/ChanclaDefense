with open("index.html", "r") as f:
    lines = f.readlines()

def print_func(func_name, end_str):
    start = -1
    for i, line in enumerate(lines):
        if func_name in line:
            start = i
            break
    if start != -1:
        end = start
        while end < len(lines):
            if end_str in lines[end]:
                break
            end += 1
        print("".join(lines[start:end+1]))

print_func("function spawnChancla()", "function addFloatText")
print_func("function drawChancla(", "function drawDialogue")
print_func("function drawChanclasAll()", "function drawWinScreen")
