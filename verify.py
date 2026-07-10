with open("index.html", "r") as f:
    content = f.read()

print("--- Anchor 1 (Variables) ---")
idx = content.find("let laserTimer = 0;")
print(content[max(0, idx - 100):min(len(content), idx + 200)])

print("\n--- Anchor 2 (Reset) ---")
idx = content.find("laser.active = false;")
print(content[max(0, idx - 100):min(len(content), idx + 200)])

print("\n--- Anchor 3 (Update) ---")
idx = content.find("if (laser.warningTimer > 0) {")
print(content[max(0, idx - 100):min(len(content), idx + 400)])

print("\n--- Anchor 4 (Draw) ---")
idx = content.find("function drawLaser()")
print(content[max(0, idx - 100):min(len(content), idx + 300)])
