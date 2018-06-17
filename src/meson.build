# These arguments are only used to build the shared library
# not the executables that use the library.
lib_args = ['-DBUILDING_PLATYPUS']

# Hiding symbols that are not explicitly marked as exported
# requires a compiler flag on all compilers except VS.
cpp = meson.get_compiler('cpp')
if cpp.get_id() != 'msvc'
  lib_args += ['-fvisibility=hidden']
endif

shlib = shared_library('platypus', 'platypus.cpp',
  install : true,
  cpp_args : lib_args,
)
