import subprocess
import time

PACKAGE = "com.starbucks.mobilecard"
APKTOOL = "~/apktool/apktool_2.6.1.jar"
APK = "~/apk/Starbucks_6.91_apkcombo.app.apk"

def run_win(command):
    print(f"[+] Running: {command}")
    result = subprocess.run(
        ["pwsh.exe", "-Command", command],
        capture_output=True,
        text=True
    )
    if result.stout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result

def run_wsl(command):
    print(f"[+] Running: {command}")
    result = subprocess.run(
        ["wsl.exe", command],
        capture_output=True,
        text=True
    )
    if result.stout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result

# Check if app is installed
check = run_win(f'adb shell cmd package list packages | grep $PACKAGE')

if check.returncode == 0:
    print(f"[+] {PACKAGE} found")
    print("[+] Uninstalling...")
    run_win(f"adb uninstall {PACKAGE}")
else:
    print(f"[-] {PACKAGE} not found")

time.sleep(1)
print()

# Patching APK
print("[+] Patching APK...")
run_wsl(f"apk-mitm --apktool {APKTOOL} {APK}")
time.sleep(1)

# Installing patched APK
print("[+] Installing...")
run_win("adb install ./apk/Starbucks_6.91_apkcombo.app-patched.apk")
print("[+] Done.")
