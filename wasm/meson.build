emrun = find_program('emrun')

plat_wasm = executable('platypus', 'wasmmain.cpp',
  dependencies: plat_dep)

htmlpage = configure_file(input: 'platypus.html',
  output: 'platypus.html',
  copy: true)

run_target('servewasm',
  command: [emrun, '--no_emrun_detect', '--no_browser', htmlpage],
  depends: plat_wasm)
