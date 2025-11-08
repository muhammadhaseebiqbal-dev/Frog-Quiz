# How to Get Android APK Crash Logs

## The problem you're seeing:
- App opens, shows loading screen, then crashes immediately
- Crashes again when you reopen it

## Option 1: Using Android Studio Logcat (BEST - Most detailed)

### Setup:
1. **Install Android Studio** (if not already installed)
   - Download from: https://developer.android.com/studio
   
2. **Enable Developer Options on your phone:**
   - Go to **Settings** → **About Phone**
   - Tap **Build Number** 7 times (until it says "You are now a developer")
   
3. **Enable USB Debugging:**
   - Go to **Settings** → **Developer Options**
   - Turn on **USB Debugging**
   
4. **Connect phone to computer via USB cable**

### Get the logs:
1. Open **Android Studio**
2. Go to **View** → **Tool Windows** → **Logcat**
3. Select your device from the dropdown at top
4. **Clear the log** (trash icon)
5. **Open your app** on the phone (let it crash)
6. In Logcat, filter by **"AndroidRuntime"** or **"python"** or **"FATAL"**
7. **Copy ALL the red error text** and send it to me

**What to look for:**
- Lines starting with `FATAL EXCEPTION`
- Python errors (ImportError, AttributeError, etc.)
- Stack traces showing which file/line failed

---

## Option 2: Using ADB (Android Debug Bridge) - Command Line

### Setup:
1. **Install ADB:**
   - **Windows**: Download Platform Tools from https://developer.android.com/studio/releases/platform-tools
   - Extract the zip, add the folder to your PATH
   
2. **Enable USB Debugging** (same as Option 1 above)

3. **Connect phone via USB**

### Get the logs:
Open PowerShell and run:

```powershell
# Check if device is connected
adb devices

# Clear old logs
adb logcat -c

# Start capturing logs (this will stream live logs)
adb logcat > crash_log.txt
```

Then:
1. **Open the app on your phone** (let it crash)
2. Press **Ctrl+C** in PowerShell to stop logging
3. Open **crash_log.txt** and send me the contents

**Better filtering (less noise):**
```powershell
# Only show errors and fatal crashes
adb logcat *:E > crash_log.txt
```

---

## Option 3: Using APK Analyzer (if app won't run at all)

If the app crashes before any code runs, it might be a packaging issue:

1. In **Android Studio**, go to **Build** → **Analyze APK**
2. Select your `.apk` file from GitHub Actions artifacts
3. Check:
   - **Missing libraries** (look for red entries in `lib/arm64-v8a/`)
   - **Size issues** (if APK is >100MB, assets might be too large)
   - **AndroidManifest.xml** errors

---

## What I need from you:

**Send me the crash log showing:**
1. The **FATAL EXCEPTION** line
2. Any **Python errors** (ImportError, ModuleNotFoundError, etc.)
3. The **stack trace** (lines showing file paths and line numbers)

Example of what I'm looking for:
```
E/AndroidRuntime: FATAL EXCEPTION: main
    Process: com.example.frogquiz, PID: 12345
    java.lang.RuntimeException: Unable to start activity
    Caused by: ImportError: No module named 'nicegui'
        at /data/app/.../main.py:1
```

---

## Quick check - Common APK issues:

Before getting logs, try these quick fixes:

### 1. **Storage space issue:**
   - Go to **Settings** → **Storage**
   - Make sure you have at least **500MB free** (your app has large video assets)

### 2. **Uninstall old version:**
   - If you installed an older test APK, uninstall it completely first
   - Settings → Apps → Frog Quiz → Uninstall
   - Restart phone
   - Install fresh APK

### 3. **Check APK actually contains assets:**
   - Rename `YourApp.apk` to `YourApp.zip`
   - Extract it
   - Look inside for `assets/` folder
   - Check if `GGF_resized.mp4` and other videos are present
   - If assets folder is empty → **Build failed to include assets**

### 4. **APK is too large (Gradle crash):**
   - Check APK size (right-click APK → Properties)
   - If it's >150MB → this explains the Gradle heap space errors we saw
   - **Solution**: Reduce video sizes or host videos externally

---

## After you send the logs:

I'll be able to tell you:
- ✅ If it's a **missing Python dependency** → I'll update `buildozer.spec`
- ✅ If **assets are missing** → I'll fix the build process
- ✅ If it's a **NiceGUI/Android incompatibility** → we'll pivot to PWA
- ✅ If it's a **memory issue** → we'll optimize assets or use CDN

---

## Emergency backup plan (if logs show unfixable issues):

**Create a PWA (Progressive Web App) instead:**
- Host the app on Railway (we just fixed that!)
- Users visit the website on their tablets
- Android lets you "Add to Home Screen" 
- Works offline with service workers
- No APK needed, works on both iOS and Android

This might be faster than debugging APK issues if your deadline is tomorrow (Sunday).

Let me know what you'd like to do! 🐸
