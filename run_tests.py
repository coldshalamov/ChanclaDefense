import subprocess
import glob

tests = glob.glob('verification/*.py')
tests = [t for t in tests if not t.endswith('__init__.py')]

for test in tests:
    print(f"Running {test}...")
    res = subprocess.run(['python3', test], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: {test}")
        print(res.stderr)
    else:
        print(f"PASSED: {test}")
