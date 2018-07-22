# The Platypus sample project

This repository contains a simple project demonstrating how to build a
program on multiple platforms. The actual code consists of one
portable library implemented in C++ but exposing a C interface. It is
built shared on all platforms that support it. In addition a platform
native GUI and all the installers, icons and other features needed to
make the app behave natively are added for each platform.

The goal is to create at least the following:

 - A GTK+ Unix app
 - A WIN32 application
 - An Objective C macOS app bundle
 - An Android application (not done yet)
 - A Swift iOS application (not done yet)

In addition to a plain application also build installers for:

 - Flatpak (not done yet)
 - MSI (not done yet)
 - macOS .dmg (not done yet)
