import re

def check_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    b9 = re.search(r"for \(const c of chanclas\) drawChancla\(ctx, c\.x, c\.y, c\.w, c\.h, c\.type, c\.rotation\);", content).group(0)
    print(f"--- {filepath} Block 9 (drawChanclasAll) ---")
    print(b9)

check_file('index.html')
check_file('chancla_bomb.html')
