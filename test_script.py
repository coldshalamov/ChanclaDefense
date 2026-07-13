import subprocess
print("Copying to chancla_bomb.html to match index.html...")
subprocess.run(["cp", "index.html", "chancla_bomb.html"])

print("Running Playwright tests...")
res = subprocess.run(["python3", "-m", "pytest", "verification/"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("ERRORS:", res.stderr)
