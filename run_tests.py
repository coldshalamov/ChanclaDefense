import subprocess
import os

test_files = [f for f in os.listdir('verification') if f.endswith('.py') and not f.startswith('__')]

for test in test_files:
    print(f"Running {test}...")
    result = subprocess.run(['python3', f'verification/{test}'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed: {test}")
        print(result.stdout)
        print(result.stderr)
    else:
        print(f"Passed: {test}")
