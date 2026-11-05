import re

for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    # Just clean up the extra whitespace from empty block
    content = content.replace("                        \n\n                        // Slap the chancla away", "                        // Slap the chancla away")

    with open(filename, 'w') as f:
        f.write(content)
