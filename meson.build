project('gkraken',
  version: run_command(
    'grep',
    'APP_VERSION',
    files('gkraken/conf.py')
  ).stdout().split(' = ')[1].strip().strip('"'),
  meson_version: '>= 0.50.0'
)
# project version is defined in gkraken/conf.py

# Importing modules
# i18n = import('i18n')
python3 = import('python3')
python = import('python3')

prefix = get_option('prefix')
PKGDATA_DIR = join_paths(prefix, get_option('datadir'), meson.project_name())
DATA_DIR = PKGDATA_DIR
PYTHON_DIR = join_paths(prefix, python.sysconfig_path('purelib'))

message('Looking for dependencies')
python_bin = python.find_python()
if not python_bin.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif

# Dependencies
dependency('gobject-introspection-1.0', version: '>= 1.56.0')

install_subdir('gkraken', install_dir: PYTHON_DIR)
install_subdir('python-xlib/Xlib', install_dir: join_paths(PYTHON_DIR, 'gkraken'))
subdir('data')
subdir('bin')

meson.add_install_script('scripts/meson_post_install.py')