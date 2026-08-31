import sys

def patch(filename, out_filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Bypass IIFE to expose internal variables, as instructed in memory.
    content = content.replace("(() => {", "window.gameApp = (() => {")
    content = content.replace("initTitle();", "initTitle(); window.internalState = {chanclas, addFloatText, trySlap, player, isa, specialAttackBar};")
    content = content.replace("let chanclas = [];", "let chanclas = window.testChanclas || [];")

    with open(out_filename, 'w', encoding='utf-8') as f:
        f.write(content)

patch("index.html", "temp_test.html")
