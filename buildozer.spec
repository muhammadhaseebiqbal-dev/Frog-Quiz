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
source.include_exts = py,png,jpg,jpeg,mp4

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,*.py

# (str) Main entry point for Android (simplified Kivy version)
# Note: main.py contains the full NiceGUI version for web deployment
# main_kivy.py is the simplified Android entry point
# Uncomment the line below to use Kivy version for APK builds
# android.entrypoint = main_kivy.py

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
requirements = python3==3.10.10,hostpython3==3.10.10,kivy==2.2.1,pyjnius,android

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

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Filename of icon
icon.filename = assets/App_overview.png

# (bool) Skip byte compile for .py files
android.no_byte_compile_python = False

# (str) Bootstrap to use
p4a.bootstrap = sdl2

# (str) Branch of python-for-android to use
p4a.branch = master

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1