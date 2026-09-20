import re

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    enrage_normal_search = """                    addFloatText('¡ENRAGED!', isa.x, isa.y - 30);
                }

                if (isa.enraged) {"""
    enrage_normal_replace = """                    addFloatText('¡ENRAGED!', isa.x, isa.y - 30);
                    triggerChanclaStorm();
                }

                if (isa.enraged) {"""
    content = content.replace(enrage_normal_search, enrage_normal_replace, 1)

    with open(filepath, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
