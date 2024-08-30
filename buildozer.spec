[app]
# (list) Application title
title = CaptchaApp
# (string) Package name
package.name = captchaapp
# (string) Package domain (needed for android/ios packaging)
package.domain = org.example
# (string) Source code where the main.py live
source.dir = .
# (list) List of inclusions using pattern matching
source.include_exts = py,png,jpg,kv,atlas
# (list) List of binaries to include
source.include_patterns = assets/*.jpg,assets/*.png
# (list) List of modules to install with pip
requirements = python3,kivy,opencv-python-headless,easyocr,requests
# (string) Path to a custom kivy directory (default: kivy)
kivy.dir = /path/to/kivy
# (string) Application version
version = 0.1
# (list) List of the main Python modules to add as source files
source.include = main.py
# (string) Application icon
icon.filename = %(source.dir)s/icon.png

[buildozer]
# (int) Target API
android.api = 30
# (int) Minimum API your APK will support
android.minapi = 21
# (int) Android SDK version to use
android.sdk = 20
# (string) Android NDK version to use
android.ndk = 21b
# (string) Android build tools version
android.build_tools = 29.0.2
# (string) Path to the Android SDK
android.sdk_path = /path/to/android-sdk
# (string) Path to the Android NDK
android.ndk_path = /path/to/android-ndk

[package]
# (string) Path to the package directory
package.dir = /path/to/package
