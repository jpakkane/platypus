#!/usr/bin/env python3

import os, sys, pathlib
import argparse
import subprocess
import shutil

ANDROID_CPU_TO_MESON_CPU: dict[str, str] = {
    'arm64-v8a': 'aarch64',
    'armv7a': 'arm',
    'i686': 'x86',
    'x86_64': 'x86_64',
    'riscv64': 'riscv64',
}

def ver2tuple(verstr):
    entries = verstr.split('.')
    return tuple([int(x) for x in entries])

class AndroidNdkBuilder:
    def __init__(self):
        self.cross_dir = pathlib.Path('android-cross')
        exe = shutil.which('meson')
        if exe is not None:
            self.meson_command = [exe]
        else:
            self.meson_command = [sys.executable, pathlib.Path.home() / 'meson/meson.py']
        self.buildtype = 'release'

    def create_crossfiles(self):
        if self.cross_dir.is_dir():
            return
        subprocess.check_call(self.meson_command + ['env2mfile', '--android', '-o', self.cross_dir])

    def build(self, options):
        self.create_crossfiles()
        self.detect_platform(options)
        self.setup_builddir()
        self.compile()
        self.install()
        self.copy_cpplib()

    def detect_platform(self, options):
        self.cpu = options.cpu
        self.meson_cpu = ANDROID_CPU_TO_MESON_CPU[self.cpu]

        self.ndk_version = self.detect_ndk_version(options)
        self.abi = self.detect_abi(options)
        print('Using CPU:', self.cpu)
        print('Using NDK:', self.ndk_version)
        print('Using ABI:', self.abi)

        self.cross_file = self.cross_dir / f'android-{self.ndk_version}-{self.abi}-{self.meson_cpu}-cross.txt'
        if not self.cross_file.is_file():
            sys.exit(f'Cross file {self.cross_file} not found.')
        self.build_dir = pathlib.Path(f'build-android-{self.ndk_version}-{self.abi}-{self.cpu}')
        self.jnilib_dir = f'jniLibs/{self.cpu}'
        self.install_root = pathlib.Path('.').absolute() / 'app/src/main'
        #print(self.install_root)

    def copy_cpplib(self):
        # If your code uses C++ it needs the C++ standard library
        # either statically linked or in a shared lib.
        # This uses the latter.
        ndk_root = self.get_ndk_root()

    def get_ndk_root(self):
        f = open(self.cross_file, 'r', encoding='utf-8')
        f.readline()
        c_compiler = f.readline()
        f.close()
        if not c_compiler.startswith('c = '):
            sys.exit('The hack solution for determining NDK root did not work. Fix things.')
        cpath = pathlib.Path(eval(c_compiler.split(' ', 2)[-1]))
        toolchain_root = cpath.parent.parent
        cpplib_dir = toolchain_root / f'sysroot/usr/lib/{self.meson_cpu}-linux-android'
        cpplib_file = cpplib_dir / 'libc++_shared.so'
        if not cpplib_file.is_file():
            sys.exit('Could not locate libc++_shared.so.')
        shutil.copy(cpplib_file, self.install_root / self.jnilib_dir)

    def install(self):
        subprocess.check_call(self.meson_command + ['install', '--destdir', self.install_root],
                              cwd=self.build_dir)

    def compile(self):
        subprocess.check_call('ninja',
                              cwd=self.build_dir)

    def setup_builddir(self):
        if self.build_dir.exists():
            return
        setup_args = ['setup',
                      '.',
                      self.build_dir,
                      '--cross-file',
                      self.cross_file,
                      f'--buildtype={self.buildtype}',
                      '--prefix=/',
                      f'--libdir={self.jnilib_dir}'
                      ]
        subprocess.check_call(self.meson_command + setup_args)

    def detect_ndk_version(self, options):
        if options.ndk_version:
            return options.ndk_version
        version_str = '0.0.0'
        version_tuple = ver2tuple(version_str)
        for f in self.cross_dir.glob(f'android-*{self.meson_cpu}-cross.txt'):
            trial_str = f.name.split('-')[1]
            trial_tuple = ver2tuple(trial_str)
            if trial_tuple > version_tuple:
                version_str = trial_str
                version_tuple = trial_tuple
        if version_str == '0.0.0':
            sys.exit('Could not detect ndk version.')
        return version_str

    def detect_abi(self, options):
        if options.abi:
            return options.abi
        abi_version = 'android00'
        for f in self.cross_dir.glob(f'android-{self.ndk_version}-*-{self.meson_cpu}-cross.txt'):
            trial_str = f.name.split('-')[2]
            if int(trial_str[-2:]) > int(abi_version[-2:]):
                abi_version = trial_str
        if abi_version == 'android00':
            sys.exit('Could not detect ABI version.')
        return abi_version

parser = argparse.ArgumentParser(description='Build and install project with Android NDK.')

parser.add_argument('--ndk-version', default=None, help='NDK version to use, defaults to newest.')
parser.add_argument('--cpu', default='arm64-v8a', help='Android CPU type to use.')
parser.add_argument('--abi', default=None, help='ABI version to use, defaults to newest.')

if __name__ == '__main__':
    opts = parser.parse_args()
    b = AndroidNdkBuilder()
    b.build(opts)
