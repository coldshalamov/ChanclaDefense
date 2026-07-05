import subprocess
import glob
import os

test_files = glob.glob('verification/*.py')
all_passed = True
for f in test_files:
    print(f"Running {f}...")
    res = subprocess.run(['python3', f], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"{f} FAILED:\n{res.stdout}\n{res.stderr}")
        all_passed = False
    else:
        print(f"{f} PASSED.")

if all_passed:
    print("All tests passed!")
else:
    print("Some tests failed.")
