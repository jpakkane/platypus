add_languages('objc')

cocoa_dep = dependency('appleframeworks', modules : ['AppKit', 'foundation'])

executable('platypus',
  'main.m', 'AppDelegate.m',
  install : true,
  objc_args : ['-fobjc-arc'],
  dependencies : [plat_dep, cocoa_dep],
)

ibtool = find_program('ibtool')

custom_target('main_nib',
  input : 'MainMenu.xib',
  output : 'MainMenu.nib',
  command : [ibtool, '--compile', '@OUTPUT@', '@INPUT@'],
  install : true,
  # This value stolen from XCode without understanding what it does.
  install_dir : 'Contents/Resources/Base.lproj',
)

install_data('Info.plist',
  install_dir : 'Contents'
  )

meson.add_install_script('otooler.py')
