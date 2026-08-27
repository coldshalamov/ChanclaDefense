import sys
import os
import re

def run():
    print("Testing Boomerang Chancla logic implementation...")

    # 1. Verify index.html contains the logic
    with open('index.html', 'r') as f:
        content = f.read()

    assert "const isBoomerang =" in content, "isBoomerang not defined in index.html"
    assert "else if (isBoomerang) { w = 34; h = 34; }" in content, "Boomerang size not in index.html"
    assert "else if (isBoomerang) type = 'boomerang';" in content, "Boomerang type not in index.html"
    assert "returning: false" in content, "returning flag not in index.html"
    assert "else if (type === 'boomerang') emoji = '🪃';" in content, "Boomerang emoji not in index.html"
    assert "c.isShrapnel || c.returning" in content, "Boundary check for returning not in index.html"
    assert "SWOOP! 🪃" in content, "Swoop behavior not in index.html"

    # 2. Verify chancla_bomb.html contains the logic
    with open('chancla_bomb.html', 'r') as f:
        content2 = f.read()

    assert "const isBoomerang =" in content2, "isBoomerang not defined in chancla_bomb.html"
    assert "SWOOP! 🪃" in content2, "Swoop behavior not in chancla_bomb.html"

    print("All Boomerang logic successfully verified!")

if __name__ == "__main__":
    run()
