import re

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The game includes a 'Ghost Chancla' mechanic where projectiles turn invisible mid-flight
    # Need to update ghost to be invisible mid-flight properly

    ghost_logic_search = """                    // Sniper Logic"""
    ghost_logic_replace = """                    // Ghost Logic
                    if (c.type === 'ghost' && !c.slapped) {
                        if (c.y > canvas.height * 0.35 && c.y < canvas.height * 0.7) {
                            c.invisible = true;
                        } else {
                            c.invisible = false;
                        }
                    }

                    // Sniper Logic"""
    content = content.replace(ghost_logic_search, ghost_logic_replace, 1)

    with open(filepath, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
