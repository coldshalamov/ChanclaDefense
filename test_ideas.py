import re
with open("index.html", "r") as f:
    content = f.read()

# Let's verify our anchor strings
print("Anchor 1 (Variables):")
print(content.find("let meteorTimer = 0;"))

print("\nAnchor 2 (Reset):")
print(content.find("meteorTimer = 0;"))

print("\nAnchor 3 (Update):")
print(content.find("if (isa.enraged) {"))

print("\nAnchor 4 (Draw):")
print(content.find("drawSpecialProjectiles();"))
