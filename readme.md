# The Platypus sample project

This repository contains a simple project demonstrating how to build a
program on multiple platforms. The actual code consists of one
portable library implemented in C++ but exposing a C interface. It is
built shared on all platforms. In addition a platform native GUI and
all the installers, icons and other features needed to make the app
behave natively are added for each platform.

The goal is to create at least the following:

 - A GTK+ Unix app
 - A WIN32 application
 - An Objective C macOS app bundle
 - An Android application
 - A Swift iOS application (not done yet)

In addition to the basic application also build installers for:

 - Flatpak
 - Windows MSI
 - macOS .dmg


## Compiling

The Flatpak application is built in the standard way with
flatpak-builder. The manifest file is in the source root.

The Windows version is built by running the `build_win.py` script from the
source root from a Visual Studio command line terminal window. It
creates a .msi installer that will be placed in the build directory.

The macOS version is built by running the `build_macos.py` script from
the source root. It creates a macOS application bundle installer that
will be placed in the build directory.

The Webassembly version can be built and started by running `ninja
servewasm`. `emrun` will then print the server URL to stdout.

The Android version can be built with the `build_android.py`
script. It builds a shared lib and places it in the source tree so
that Android Studio picks it up automatically.
