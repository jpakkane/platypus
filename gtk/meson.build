add_languages('c')

# Since there is only one file, build a direct path.
# In a bigger project you'd build a path to the datadir
# and then do the file name concatenation in your program
# code instead.

gladeloc = join_paths(get_option('prefix'),
         get_option('datadir'),
         'platypus/platygui.glade')

executable('platypus',
  'gtkapp.c',
  c_args : ['-DGLADE_FILE="@0@"'.format(gladeloc)],
  dependencies : [plat_dep, gtk_dep],
  install : true)

install_data('platygui.glade',
  install_dir : join_paths(get_option('datadir'), 'platypus'))

install_subdir('icons', install_dir : get_option('datadir'))

install_data('io.github.jpakkane.platypus.desktop',
  install_dir : join_paths(get_option('datadir'), 'applications'))

install_data('io.github.jpakkane.platypus.appdata.xml',
  install_dir : join_paths(get_option('datadir'), 'metainfo'))
