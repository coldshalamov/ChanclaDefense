import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_handle_mobile = """            function handleMobileZones(zone, dir) {
                zone.addEventListener('touchstart', (e) => {
                    if (state !== STATE.PLAYING) return;
                    touch[dir] = true;
                    e.preventDefault();
                }, { passive: false });
                zone.addEventListener('touchend', () => { touch[dir] = false; });
                zone.addEventListener('touchcancel', () => { touch[dir] = false; });
            }"""

    new_handle_mobile = """            let lastTouch = '';
            let lastTouchTime = 0;
            function handleMobileZones(zone, dir) {
                zone.addEventListener('touchstart', (e) => {
                    if (state !== STATE.PLAYING) return;

                    if (lastTouch === dir && Date.now() - lastTouchTime < 300 && player.dashCooldown <= 0) {
                        player.dashTimer = 0.3;
                        player.dashCooldown = 1.0;
                        player.dashDir = dir === 'left' ? -1 : 1;
                    }
                    lastTouch = dir;
                    lastTouchTime = Date.now();

                    touch[dir] = true;
                    e.preventDefault();
                }, { passive: false });
                zone.addEventListener('touchend', () => { touch[dir] = false; });
                zone.addEventListener('touchcancel', () => { touch[dir] = false; });
            }"""

    if old_handle_mobile in content:
        content = content.replace(old_handle_mobile, new_handle_mobile, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Done")
