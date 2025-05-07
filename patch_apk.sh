#!/bin/bash

PACKAGE="com.starbucks.mobilecard"
APKTOOL="./apktool/apktool_2.6.1.jar"
APK="./apk/Starbucks_6.91_apkcombo.app.apk"

# Removing old application
IS_INSTALLED=$(adb shell cmd package list packages | grep $PACKAGE)
if [ $IS_INSTALLED ] ; then
    echo "[+] $PACKAGE found"
    echo "[+] Uninstalling..."
    adb uninstall $PACKAGE
fi
sleep 1
echo

# Patching APK to remove certificate pinning
echo "[+] Patching APK..."
apk-mitm --apktool $APKTOOL $APK
sleep 1

# Installing patched application
echo "[+] Installing..."
adb install ./apk/Starbucks_6.91_apkcombo.app-patched.apk
echo "[+] Done."
