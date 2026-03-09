import sys

def patch_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Add lastTap variables
    old_keys = "const keys = { left: false, right: false };"
    new_keys = """let lastLeftTap = 0;
            let lastRightTap = 0;
            const keys = { left: false, right: false };"""

    if old_keys in content:
        content = content.replace(old_keys, new_keys)
        print(f"Patched keys in {filename}")
    else:
        print(f"Could not find keys in {filename}")

    # Patch handleKey
    old_handle_key = """            function handleKey(e, isDown) {
                if (['ArrowLeft', 'a', 'A'].includes(e.key)) { keys.left = isDown; e.preventDefault(); }
                if (['ArrowRight', 'd', 'D'].includes(e.key)) { keys.right = isDown; e.preventDefault(); }"""

    new_handle_key = """            function handleKey(e, isDown) {
                if (['ArrowLeft', 'a', 'A'].includes(e.key)) {
                    if (isDown && !keys.left && player.dashCooldown <= 0) {
                        let now = performance.now() / 1000;
                        if (now - lastLeftTap < 0.3) {
                            player.dashTimer = 0.3;
                            player.dashCooldown = 1.0;
                            player.dashDir = -1;
                            lastLeftTap = 0; // Reset
                        } else {
                            lastLeftTap = now;
                        }
                    }
                    keys.left = isDown;
                    e.preventDefault();
                }
                if (['ArrowRight', 'd', 'D'].includes(e.key)) {
                    if (isDown && !keys.right && player.dashCooldown <= 0) {
                        let now = performance.now() / 1000;
                        if (now - lastRightTap < 0.3) {
                            player.dashTimer = 0.3;
                            player.dashCooldown = 1.0;
                            player.dashDir = 1;
                            lastRightTap = 0; // Reset
                        } else {
                            lastRightTap = now;
                        }
                    }
                    keys.right = isDown;
                    e.preventDefault();
                }"""

    if old_handle_key in content:
        content = content.replace(old_handle_key, new_handle_key)
        print(f"Patched handleKey in {filename}")
    else:
        print(f"Could not find old_handle_key in {filename}")

    # Patch handleMobileZones
    old_handle_mobile = """            function handleMobileZones(zone, dir) {
                zone.addEventListener('touchstart', (e) => {
                    if (state !== STATE.PLAYING) return;
                    touch[dir] = true;
                    e.preventDefault();
                }, { passive: false });
                zone.addEventListener('touchend', () => { touch[dir] = false; });
                zone.addEventListener('touchcancel', () => { touch[dir] = false; });
            }"""

    new_handle_mobile = """            function handleMobileZones(zone, dir) {
                zone.addEventListener('touchstart', (e) => {
                    if (state !== STATE.PLAYING) return;
                    if (!touch[dir] && player.dashCooldown <= 0) {
                        let now = performance.now() / 1000;
                        if (dir === 'left') {
                            if (now - lastLeftTap < 0.3) {
                                player.dashTimer = 0.3;
                                player.dashCooldown = 1.0;
                                player.dashDir = -1;
                                lastLeftTap = 0;
                            } else { lastLeftTap = now; }
                        } else {
                            if (now - lastRightTap < 0.3) {
                                player.dashTimer = 0.3;
                                player.dashCooldown = 1.0;
                                player.dashDir = 1;
                                lastRightTap = 0;
                            } else { lastRightTap = now; }
                        }
                    }
                    touch[dir] = true;
                    e.preventDefault();
                }, { passive: false });
                zone.addEventListener('touchend', () => { touch[dir] = false; });
                zone.addEventListener('touchcancel', () => { touch[dir] = false; });
            }"""

    if old_handle_mobile in content:
        content = content.replace(old_handle_mobile, new_handle_mobile)
        print(f"Patched handleMobileZones in {filename}")
    else:
        print(f"Could not find old_handle_mobile in {filename}")


    with open(filename, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
