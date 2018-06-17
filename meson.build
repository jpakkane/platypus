project('platypus', 'cpp',
  version : '0.1.0',
  default_options : ['warning_level=3', 'cpp_std=c++14'])

subdir('src')

gtk_dep = dependency('gtk+-3.0')
subdir('gtk', if_found : gtk_dep)
