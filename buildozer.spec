[app]

# (str) Title of your application
title = Frog Quiz

# (str) Package name
package.name = frogquiz

# (str) Package domain (needed for android/ios packaging)
package.domain = org.katiehoward

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
# Include full-size _resized.mp4 videos for best quality
# IMPORTANT: json extension needed for lazy loading screen configuration
source.include_exts = py,png,jpg,jpeg,mp4,json

# (list) List of inclusions using pattern matching  
# Include all _resized.mp4 (full-size videos) for APK
source.include_patterns = assets/*.png,assets/*.jpg,assets/*_resized.mp4

# (list) Source files to exclude (let empty to not exclude anything)
# CRITICAL: Exclude main_web.py (NiceGUI web app) - main.py is the Kivy Android app
source.exclude_patterns = main_web.py,buildozer_hook.py,main_activity.py,uvicorn_config.py,Procfile,Dockerfile,compress*.py,VIDEO_COMPRESSION_GUIDE.py

# (str) Main entry point for Android (Java/Kotlin activity class name)
# Note: Keep the Python entry filename as `main_kivy.py` in the app source,
# but the Android manifest must reference the activity class. Use the
# standard Kivy activity so the system doesn't try to instantiate a Python
# filename as a Java class.
android.entrypoint = org.kivy.android.PythonActivity

# (str) Application versioning (method 1)
version = 1.0

# (str) Supported orientation (landscape, portrait or all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# (list) Application requirements
# Simplified to only Kivy basics - NiceGUI doesn't work well with P4A
requirements = python3==3.10.10,hostpython3==3.10.10,kivy==2.2.1,pyjnius,android,ffpyplayer

# (str) The Android arch to build for
android.archs = arm64-v8a

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Filename of icon
icon.filename = assets/App_overview.png

# (bool) Skip byte compile for .py files
android.no_byte_compile_python = False

# (str) Bootstrap to use
p4a.bootstrap = sdl2

# (str) Branch of python-for-android to use
p4a.branch = master

# (str) Hook for gradle (inject gradle.properties with memory settings)
android.gradle_dependencies = 
p4a.hook = buildozer_hook.py

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1