import subprocess
import glob
files = glob.glob("verification/test_*.py") + glob.glob("verification/verify_*.py")
for f in files:
    print(f"Running {f}...")
    subprocess.run(["python3", f], check=False)
