#!/usr/bin/env python3

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
