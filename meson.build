project('platypus', 'cpp',
  version : '0.1.0',
  meson_version: '>=0.51.99',
  default_options : ['warning_level=3', 'cpp_std=c++14'])

if host_machine.system() == 'wasm'
  add_global_arguments('-s', 'EXPORT_ALL=1', language: 'cpp')
  add_global_link_arguments('-s', 'EXPORT_ALL=1', language: 'cpp')
endif

subdir('src')

gtk_dep = dependency('gtk+-3.0', required : false)
subdir('gtk', if_found : gtk_dep)

if host_machine.system() == 'darwin'
  subdir('macOS')
endif

if host_machine.system() == 'windows'
  subdir('windows')
  c = configuration_data()
  c.set('VERSION', meson.project_version())
  configure_file(input : 'windows/platypus.json.in',
    output : 'platypus.json',
    configuration : c)
endif

if host_machine.cpu_family().startswith('wasm')
  subdir('wasm')
endif
