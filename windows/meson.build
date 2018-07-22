wm = import('windows')

executable('platypus',
  'main.cpp',
  wm.compile_resources('platypus.rc'),
  extra_files : 'platypus.rc', # HACK
  install : true,
  gui_app : true,
  dependencies : plat_dep,
  )

install_data('License.rtf', install_dir : get_option('prefix'))
