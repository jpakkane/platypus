# The Platypus sample project

This repository contains a simple project demonstrating how to build a
program on multiple platforms. The actual code consists of one
portable library implemented in C++ but exposing a C interface. It is
built shared on all platforms that support it. In addition a platform
native GUI and all the installers, icons and other features needed to
make the app behave natively are added for each platform.

The goal is to create at least the following:

 - A GTK+ Flatpak app (not done yet)
 - A WIN32 application with an msi installer (not done yet)
 - An Objective C macOS application in an app bundle (not done yet)
 - An Android application (not done yet)
 - An iOS application (not done yet)
