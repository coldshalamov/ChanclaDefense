import subprocess
import os

files = os.listdir("verification")
for f in files:
    if f.endswith(".py"):
        print(f"Running {f}...")
        try:
            subprocess.run(["python3", os.path.join("verification", f)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed {f}")
