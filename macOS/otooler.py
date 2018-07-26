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

import os, sys, subprocess

install_dir = os.environ['MESON_INSTALL_PREFIX']

exename = os.path.join(install_dir, 'Contents/MacOS/platypus')

otoolout = subprocess.check_output(['otool', '-L', exename], universal_newlines=True)

for line in otoolout.split('\n'):
    line = line.strip()
    if line.startswith(install_dir) and exename not in line:
        libname = line.split(' ', 1)[0]
        rel_name = '@executable_path/' + os.path.split(libname)[1]
        subprocess.check_call(['install_name_tool', '-change', libname, rel_name, exename])
