def get_trySlap():
    with open('index.html', 'r') as f:
        content = f.read()

    start = content.find('function trySlap() {')
    end = content.find('function fireSpecialAttack() {')
    print(content[start:end])

get_trySlap()
