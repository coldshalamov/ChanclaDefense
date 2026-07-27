import subprocess
import glob

tests = glob.glob('verification/*.py')
success = True
for test in tests:
    print(f"Running {test}...")
    res = subprocess.run(['python3', test], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED {test}")
        print(res.stdout)
        print(res.stderr)
        success = False

if success:
    print("All tests passed!")
else:
    print("Some tests failed!")
