import setuptools

from gkraken.conf import APP_PACKAGE_NAME, APP_VERSION, APP_SOURCE_URL, APP_AUTHOR, APP_AUTHOR_EMAIL

# with open('README.md', 'r', encoding='utf-8') as fh:
#     long_description = (fh.read().split('<!-- stop here for PyPI -->', 1)[0]
#                         + 'Check the project page page for more information.')

setuptools.setup(
    name=APP_PACKAGE_NAME,
    version=APP_VERSION,
    description='GUI to control cooling and lighting of NZXT Kraken X (X42, X52, X62 or X72) pumps',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url=APP_SOURCE_URL,
    author=APP_AUTHOR,
    author_email=APP_AUTHOR_EMAIL,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: System :: Hardware',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
    keywords='nzxt kraken',
    packages=setuptools.find_packages(),
    package_data={
        # If any package contains *.txt files, include them:
        '': ['*.txt'],
        # And include any *.dat files found in the 'data' subdirectory
        # of the 'mypkg' package, also:
        APP_PACKAGE_NAME: ['data/gkraken.glade'],
    },
    project_urls={
        'Source': APP_SOURCE_URL,
        'Tracker': APP_SOURCE_URL + '/issues',
        'Changelog': '{}/blob/{}/CHANGELOG.md'.format(APP_SOURCE_URL, APP_VERSION),
        'Documentation': '{}/blob/{}/README.md'.format(APP_SOURCE_URL, APP_VERSION),

    },
    install_requires=[
        'injector==0.14.1',
        'liquidctl==1.0.0',
        'matplotlib==3.0.0',
        'peewee==3.7.0',
        'pyxdg',
        'rx==1.6.1',
    ],
    python_requires='~=3.6',
    entry_points={
        'console_scripts': [
            'gkraken=gkraken.main:main',
        ],
    },
)
