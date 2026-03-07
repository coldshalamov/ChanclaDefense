import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_handle_key = """            function handleKey(e, isDown) {
                if (['ArrowLeft', 'a', 'A'].includes(e.key)) { keys.left = isDown; e.preventDefault(); }
                if (['ArrowRight', 'd', 'D'].includes(e.key)) { keys.right = isDown; e.preventDefault(); }"""

    new_handle_key = """            let lastKey = '';
            let lastKeyTime = 0;
            function handleKey(e, isDown) {
                if (isDown && ['ArrowLeft', 'a', 'A', 'ArrowRight', 'd', 'D'].includes(e.key)) {
                    if (state === STATE.PLAYING && lastKey === e.key && Date.now() - lastKeyTime < 300 && player.dashCooldown <= 0) {
                        player.dashTimer = 0.3;
                        player.dashCooldown = 1.0;
                        player.dashDir = ['ArrowLeft', 'a', 'A'].includes(e.key) ? -1 : 1;
                    }
                    lastKey = e.key;
                    lastKeyTime = Date.now();
                }

                if (['ArrowLeft', 'a', 'A'].includes(e.key)) { keys.left = isDown; e.preventDefault(); }
                if (['ArrowRight', 'd', 'D'].includes(e.key)) { keys.right = isDown; e.preventDefault(); }"""

    if old_handle_key in content:
        content = content.replace(old_handle_key, new_handle_key, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Done")
