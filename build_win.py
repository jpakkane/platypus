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

def delete_junk(staging_dir):
    # In the real world you'd move the pdb files
    # et al to storage. For now just delete them.
    for pattern in ('*.ilk', '*.pdb', '*.lib'):
        for f in pathlib.Path(staging_dir).glob(pattern):
            f.unlink()

def do_it(meson_command):
    builddir = 'build-release'
    staging_dir = os.path.join(os.getcwd(), builddir, 'staging')
    if os.path.exists(builddir):
        shutil.rmtree(builddir)
    args = [builddir,
            '--buildtype=debugoptimized',
            '--prefix=' + staging_dir,
            '--libdir=',
            '--bindir=',
            '--backend=ninja',
            ]
    subprocess.check_call(meson_command + args)
    subprocess.check_call(['ninja', '-C', builddir])
    subprocess.check_call(['ninja', '-C', builddir, 'test'])
    subprocess.check_call(['ninja', '-C', builddir, 'install'])

    delete_junk(staging_dir)
    subprocess.check_call([sys.executable,
                           '../msicreator/createmsi.py',
                           'platypus.json'],
                          cwd=builddir)
    print('The MSI installer can be found in build directory %s.' % builddir)

def get_msicreator():
    # Once MsiCreator is in pip, use that one instead.
    if os.path.exists('msicreator'):
        subprocess.check_call(['git', 'pull'], cwd='msicreator')
    else:
        subprocess.check_call(['git',
                               'clone',
                               'https://github.com/jpakkane/msicreator.git'])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        meson_exe = autodetect_meson()
    elif len(sys.argv) == 2:
        m = sys.argv[1]
        if m.endswith('.py'):
            p = shutil.which('python')
            if p is None:
                sys.exit('Could not find Python.')
            meson_exe = [p, m]
        else:
            meson_exe = [m]
    else:
        sys.exit('This command takes at most one argument.')
    get_msicreator()
    do_it(meson_exe)
