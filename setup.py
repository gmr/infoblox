from setuptools import setup

requirements = ['requests']
tests_require = ['mock', 'httmock']
try:
    import argparse
except ImportError:
    requirements.append('argparse')
    tests_require.append('unittest2')

classifiers = ['Intended Audience :: Developers',
               'Intended Audience :: System Administrators',
               'License :: OSI Approved :: BSD License',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.3',
               'Topic :: Communications',
               'Topic :: Internet',
               'Topic :: Internet :: Name Service (DNS)',
               'Topic :: Software Development :: Libraries',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Topic :: System :: Networking',
               'Topic :: System :: Systems Administration']

setup(name='infoblox',
      version='1.1.0',
      description='Interface and CLI application for Infoblox NIOS',
      long_description=open('README.rst').read(),
      author='Gavin M. Roy',
      author_email='gavinmroy@gmail.com',
      url='https://github.com/gmr/infoblox',
      packages=['infoblox'],
      package_data={'': ['LICENSE', 'README.md']},
      include_package_data=True,
      install_requires=requirements,
      license=open('LICENSE').read(),
      entry_points={'console_scripts': ['infoblox-host=infoblox.cli:main']},
      classifiers=classifiers,
      tests_require=tests_require,
      zip_safe=True)
