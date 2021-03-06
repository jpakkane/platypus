#!/usr/bin/env python3

# Copyright 2018 Jussi Pakkanen
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''Configures, builds, tests and creates an MSI installer
for the Platypus sample application using msicreator,
which in turn uses WiX.'''

import os, sys, subprocess
import shutil, pathlib

def autodetect_meson():
    for i in ('meson', 'meson.py'):
        x = shutil.which(i)
        if x is not None:
            return [x]
        sys.exit('Could not autodetect Meson. Specify it manually with a command line argument.')

def build(meson_command, builddir, staging_dir):
    if os.path.exists(builddir):
        shutil.rmtree(builddir)
    # NOTE: the end result is not stripped.
    args = [builddir,
            '--buildtype=debugoptimized',
            '--prefix=' + staging_dir,
            '--bindir=Contents/MacOS',
            '--libdir=Contents/MacOS',
            '--backend=ninja',
            ]
    subprocess.check_call(meson_command + args)
    subprocess.check_call(['ninja', '-C', builddir])
    subprocess.check_call(['ninja', '-C', builddir, 'test'])
    subprocess.check_call(['ninja', '-C', builddir, 'install'])

def create_dmg(builddir, staging_dir):
    abs_build = os.path.join(os.getcwd(), builddir)
    template = 'macOS/template.dmg.gz'
    raw_dmg = os.path.join(builddir, 'temporary.dmg')
    mountpoint = os.path.join(abs_build, 'mnttmp')
    appdir = os.path.join(mountpoint, 'platypus.app')
    final_dmg = os.path.join(builddir, 'platypus.dmg')
    subprocess.check_call('gunzip < %s > %s' % (template, raw_dmg),
                          shell=True)
    subprocess.check_call(['hdiutil',
                           'attach',
                           raw_dmg,
                           '-noautoopen',
                           '-quiet',
                           '-mountpoint',
                           mountpoint,
                           ])
    os.rmdir(appdir)
    shutil.move(staging_dir, mountpoint)
    subprocess.check_call(['hdiutil', 'detach', mountpoint])
    subprocess.check_call(['hdiutil',
                           'convert',
                           raw_dmg,
                           '-quiet',
                           '-format',
                           'UDZO',
                           '-imagekey',
                           'zlib-level=9',
                           '-o',
                           final_dmg,
                           ])
    os.unlink(raw_dmg)


def do_it(meson_command):
    builddir = 'build-macos'
    staging_dir = os.path.join(os.getcwd(), builddir, 'platypus.app')
    build(meson_command, builddir, staging_dir)
    create_dmg(builddir, staging_dir)
    print('The app dmg can be found in the build dir.')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        meson_exe = autodetect_meson()
    elif len(sys.argv) == 2:
        meson_exe = [sys.argv[1]]
    else:
        sys.exit('This command takes at most one argument.')
    do_it(meson_exe)

# Dmg template created with these instructions:
#
# https://el-tramo.be/blog/fancy-dmg/
