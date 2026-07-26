import subprocess
import glob
import sys

def main():
    scripts = glob.glob('verification/test_*.py') + glob.glob('verification/verify_*.py')
    success = True
    for script in scripts:
        print(f"Running {script}...")
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running {script}:\n{result.stderr}")
            success = False
        else:
            print(f"{script} passed.")
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
