# Testing Guide: Lazy Loading Implementation

## Quick Test Commands

### 1. Desktop Testing (Fastest)
```bash
cd "d:\WORK\Pyhton Mobile\NiceGUI-20251108T095609Z-1-001\NiceGUI"
python main.py
```

**Expected Results**:
- Home screen appears in <1 second
- No error messages in console
- Click any frog → detail screen loads smoothly
- Click Instructions → loads and displays
- Click Mystery Frog → quiz screen loads
- Videos play when clicking play button

**Console Output Should Show**:
```
Loading screen: home
✓ Screen 'home' loaded successfully
[User clicks frog]
Loading screen: frog
✓ Screen 'frog' loaded successfully
```

### 2. Build APK (Full Test)
```bash
# Clean build to ensure all changes included
buildozer android clean

# Build debug APK
buildozer android debug

# Install on connected device
adb install -r bin/FrogQuiz-1.0-arm64-v8a-debug.apk
```

### 3. Monitor App Performance on Device
```bash
# Watch for loading messages
adb logcat | grep -E "(Loading screen|Screen.*loaded|python)"

# Watch for crashes
adb logcat | grep -E "(FATAL|AndroidRuntime)"

# Full detailed log
adb logcat -s python:D SDL:D *:E
```

## Test Checklist

### Startup Performance ✅
- [ ] App icon tap → home screen in <2 seconds
- [ ] No blank/black screen longer than 2 seconds
- [ ] All 10 buttons visible immediately (8 frogs + instructions + mystery)
- [ ] No crashes during startup

### Navigation Tests ✅
- [ ] Click "Instructions" → screen loads smoothly
- [ ] Click back arrow → returns to home
- [ ] Click any frog button → detail screen loads
- [ ] Frog name and species display correctly
- [ ] Click back arrow → returns to home
- [ ] Click "Mystery Frog" → quiz screen loads
- [ ] Quiz shows 4 answer buttons
- [ ] Click back arrow → returns to home
- [ ] Click "App Info" → info screen loads
- [ ] Click back arrow → returns to home

### Video Playback Tests ✅
- [ ] Select a frog → video thumbnail visible
- [ ] Click play button → video starts playing
- [ ] Video shows spectrogram animation
- [ ] Audio plays (frog call sound)
- [ ] Click pause button → video pauses
- [ ] Click play again → video resumes
- [ ] No ANR (Application Not Responding) errors
- [ ] No SDL2 audio crashes

### Mystery Quiz Tests ✅
- [ ] Mystery screen loads new random frog
- [ ] Video shows spectrogram
- [ ] Click play → video plays
- [ ] Select wrong answer → shows ❌ message
- [ ] Click "Try Again" → new quiz loads
- [ ] Select correct answer → shows ✅ message
- [ ] Click back arrow → returns to home

### Memory & Performance ✅
- [ ] First screen load takes <2 seconds
- [ ] Subsequent screen switches are instant (<0.5s)
- [ ] App doesn't lag or stutter
- [ ] No memory warning messages in logcat
- [ ] App doesn't crash after multiple screen switches

## Debugging Common Issues

### Issue: "Module 'screens.home_screen' not found"
**Cause**: screens/ directory not included in APK  
**Fix**: Check buildozer.spec includes `source.include_exts = py,json`  
**Test**: `buildozer android clean && buildozer android debug`

### Issue: "FileNotFoundError: screens.json"
**Cause**: JSON file not packaged in APK  
**Fix**: Verify `source.include_exts` has `json` extension  
**Test**: Check if json is in `source.include_exts = py,png,jpg,jpeg,mp4,json`

### Issue: Blank screen on startup
**Cause**: Android-specific UI refresh issue  
**Fix**: Already implemented `_force_refresh()` method  
**Test**: Should resolve automatically after 0.5s

### Issue: Video doesn't play
**Cause**: SDL2 audio driver issue (AAudio crashes)  
**Fix**: Already implemented OpenSL ES driver  
**Verify**: Check `os.environ['SDL_AUDIODRIVER'] = 'opensles'` in main.py

### Issue: Screen loads but looks broken
**Cause**: Missing image/asset file  
**Fix**: Verify `assets/` directory included in APK  
**Test**: Check `source.include_patterns = assets/*.png,assets/*.jpg,assets/*_resized.mp4`

## Performance Benchmarking

### Measure Startup Time
```bash
# Clear logcat
adb logcat -c

# Start app
adb shell am start -n org.katiehoward.frogquiz/org.kivy.android.PythonActivity

# Check timestamps
adb logcat -d | grep -E "(START|python|Screen.*loaded)"
```

**Calculate**: Time from "START" to "Screen 'home' loaded successfully"  
**Target**: <2 seconds

### Monitor Memory Usage
```bash
# Get process ID
adb shell ps | grep frogquiz

# Monitor memory (replace PID)
adb shell dumpsys meminfo <PID>
```

**Look for**: 
- **Initial PSS**: Should be ~15-20 MB (down from ~30-40 MB before)
- **No memory leaks**: Memory shouldn't grow significantly during navigation

## Success Criteria

### PASS ✅
- Startup time: <2 seconds to home screen
- First-time screen load: <500ms additional delay
- Cached screen load: <50ms (instant)
- No crashes during navigation
- Videos play without SDL2 audio crashes
- Memory usage: ~15-20 MB initial (vs ~30-40 MB before)

### FAIL ❌
- Startup time: >3 seconds
- Module import errors
- Black screen >3 seconds
- App crashes when navigating
- Videos cause ANR errors
- Memory usage: >40 MB initial

## Rollback Plan

If lazy loading causes issues:

1. **Restore old main.py**:
   ```bash
   git checkout main.py
   ```

2. **Remove new files**:
   ```bash
   rm -rf screens/
   rm screens.json
   rm lazy_manager.py
   ```

3. **Revert buildozer.spec**:
   Remove `json` from `source.include_exts`

4. **Rebuild**:
   ```bash
   buildozer android clean
   buildozer android debug
   ```

## Next Steps After Testing

### If All Tests Pass ✅
1. Update version in buildozer.spec: `version = 1.1`
2. Build release APK: `buildozer android release`
3. Sign and publish APK
4. Document performance improvements for users

### If Issues Found ❌
1. Check error messages in logcat
2. Verify file structure matches documentation
3. Test on desktop first (python main.py)
4. Review LAZY_LOADING_IMPLEMENTATION.md
5. Ask for help with specific error messages

## Test Report Template

```
LAZY LOADING TEST REPORT
Date: ___________
Device: ___________
Android Version: ___________

STARTUP PERFORMANCE:
[ ] Startup time: _____ seconds (target: <2s)
[ ] Black screen duration: _____ seconds (target: <2s)
[ ] Initial memory: _____ MB (target: <25 MB)

NAVIGATION:
[ ] Home → Instructions: _____ (PASS/FAIL)
[ ] Home → Frog Detail: _____ (PASS/FAIL)
[ ] Home → Mystery Quiz: _____ (PASS/FAIL)
[ ] Home → App Info: _____ (PASS/FAIL)
[ ] Back button works: _____ (PASS/FAIL)

VIDEO PLAYBACK:
[ ] Frog detail video plays: _____ (PASS/FAIL)
[ ] Mystery quiz video plays: _____ (PASS/FAIL)
[ ] No SDL2 crashes: _____ (PASS/FAIL)
[ ] No ANR errors: _____ (PASS/FAIL)

OVERALL RESULT: _____ (PASS/FAIL)

NOTES:
______________________________________
______________________________________
```

---

**Ready to test?** Start with desktop testing, then build APK! 🚀
