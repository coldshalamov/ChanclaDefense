import sys

def get_block(filepath, start_str, end_str):
    with open(filepath, 'r') as f:
        content = f.read()
    start_idx = content.find(start_str)
    if start_idx == -1:
        print(f"Start string not found: {start_str}")
        return
    end_idx = content.find(end_str, start_idx)
    if end_idx == -1:
        print(f"End string not found: {end_str}")
        return
    print(content[start_idx:end_idx + len(end_str)])

get_block('index.html', "                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 40);\n                ctx.restore();\n            }", "                ctx.fillText('Back / Volver', canvas.width / 2, canvas.height - 40);\n                ctx.restore();\n            }")
print("\n---24---\n")

get_block('index.html', "                        // Add float text\n                        if (isPerfect) {", "                            playSound(600, 0.1);\n                        }")
print("\n---25---\n")
