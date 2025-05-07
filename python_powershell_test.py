import subprocess
import time

PACKAGE = "com.samsung.android.video"

def run(command):
    print(f"[+] Running: {command}")
    result = subprocess.run(
        ["pwsh.exe", "-Command", command],
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result

# Check if app is installed
full_command = f'adb shell cmd package list packages | Select-String "{PACKAGE}"'
check = run(full_command)

check

if check == False:
    print(f"[+] {PACKAGE} found")
else:
    print(f"[-] {PACKAGE} not found")
