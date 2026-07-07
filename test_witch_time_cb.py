import re
import os
import sys

def verify_witch_time():
    with open('chancla_bomb.html', 'r') as f:
        content = f.read()

    assert 'let witchTimeTimer = 0;' in content, "witchTimeTimer missing"
    assert 'const enemyDt = witchTimeTimer > 0 ? dt * 0.3 : dt;' in content, "enemyDt missing"
    assert 'witchTimeTimer -= dt;' in content, "witchTimeTimer update missing"
    assert 'updateChanclas(enemyDt);' in content, "updateChanclas not using enemyDt"
    assert "ctx.fillStyle = 'rgba(128, 0, 128, 0.2)';" in content, "Purple overlay missing"
    assert "witchTimeTimer = 2.0;" in content, "Perfect dodge trigger missing"

    print("All static checks passed for chancla_bomb.html!")

verify_witch_time()
