project('platypus', 'cpp',
  version : '0.1.0',
  default_options : ['warning_level=3', 'cpp_std=c++14'])

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
