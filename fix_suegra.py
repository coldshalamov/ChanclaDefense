import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the ReferenceError caused by bad replacement
# Original code had: `let specialReadyTriggered = false;`
# Our first patch replaced it with:
#             let specialReadyTriggered = false;
#             suegraTimer = 0;
#             suegra.active = false;
#
#             let suegraTimer = 0;
#             const suegra = { x: 0, y: 150, active: false, speed: 100, dropTimer: 0, hoverOffset: 0 };
# But actually the replace string matched multiple places because we replaced `specialReadyTriggered = false;` without `let`.

bad_globals = """            let
                specialReadyTriggered = false;
                suegraTimer = 0;
                suegra.active = false;


            let suegraTimer = 0;
            const suegra = { x: 0, y: 150, active: false, speed: 100, dropTimer: 0, hoverOffset: 0 };"""

content = content.replace(bad_globals, """            let specialReadyTriggered = false;
            let suegraTimer = 0;
            const suegra = { x: 0, y: 150, active: false, speed: 100, dropTimer: 0, hoverOffset: 0 };""")

bad_reset_1 = """                specialReadyTriggered = false;
                suegraTimer = 0;
                suegra.active = false;


                    // Play special attack sound"""

content = content.replace(bad_reset_1, """                specialReadyTriggered = false;
                    // Play special attack sound""")

with open('index.html', 'w') as f:
    f.write(content)
